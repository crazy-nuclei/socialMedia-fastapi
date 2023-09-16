from fastapi import status, HTTPException, Depends, APIRouter
from typing import List, Optional
from sqlalchemy import func
from sqlalchemy.orm import Session
from .. import models, schemas, oauth2
from ..database import get_db

router = APIRouter(prefix="/posts", tags=["Posts"])

@router.get("", response_model= List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db), current_user: schemas.UserOut= Depends(oauth2.get_current_user), limit: int = 10, page: int = 0, search: Optional[str]=""):
    # cursor.execute(""" select * from posts """)
    # posts = cursor.fetchall()
    # (select posts.*, count(vote.post_id) from posts 
    # left join votes on posts.id == votes.post_id)
    # group by posts.id

    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Post.id == models.Vote.post_id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(page*limit).all()

    return posts


@router.post("", status_code= status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: schemas.UserOut= Depends(oauth2.get_current_user)):
    # cursor.execute(""" insert into posts (title, content, published) values(%s, %s, %s) returning * """, (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()

    new_post = models.Post(owner_id = current_user.id ,**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


@router.get("/{id}", response_model=schemas.PostOut)
def get_post_by_id(id: int, db: Session = Depends(get_db), current_user: schemas.UserOut= Depends(oauth2.get_current_user)): 
    # cursor.execute(""" select * from posts where id = %s """, (str(id),))
    # post = cursor.fetchone()
    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Post.id == models.Vote.post_id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException( status_code= status.HTTP_404_NOT_FOUND, 
                             detail = f"post with id: {id} does not exist")
    return post


@router.delete('/{id}', status_code= status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: schemas.UserOut= Depends(oauth2.get_current_user)): 
    # cursor.execute(""" delete from posts where id = %s returning * """, (str(id),))
    # post = cursor.fetchone()
    # conn.commit()
    post_q = db.query(models.Post).filter(models.Post.id == id)

    post = post_q.first()
    if post == None: 
        raise HTTPException( status_code= status.HTTP_404_NOT_FOUND,
                            detail= f"post with id: {id} does not exist")
    
    if post.owner_id != current_user.id: 
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail=f"Not authorized to complete this action")

    post_q.delete(synchronize_session=False)
    db.commit()
    return 


@router.put('/{id}', response_model=schemas.Post)
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db), current_user: schemas.UserOut= Depends(oauth2.get_current_user)):

    # cursor.execute(""" update posts set title= %s, content= %s, published= %s  where id = %s returning * """, (post.title, post.content, post.published, str(id)))
    # updated_post = cursor.fetchone()
    # conn.commit()

    post_q = db.query(models.Post).filter(models.Post.id == id)

    post_l = post_q.first()
    if not post_l: 
        raise HTTPException( status_code= status.HTTP_404_NOT_FOUND,
                            detail= f"post with id: {id} does not exist")
    
    if post_l.owner_id != current_user.id: 
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail=f"Not authorized to complete this action")
    
    post_q.update(post.model_dump(), synchronize_session= False)
    db.commit()
    return post_q.first()