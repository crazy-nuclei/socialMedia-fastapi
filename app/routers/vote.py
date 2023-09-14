from fastapi import status, HTTPException, Depends, APIRouter
from typing import List, Optional
from sqlalchemy.orm import Session
from .. import models, schemas, oauth2
from ..database import get_db

router = APIRouter(prefix="/votes", tags=["Vote"])



@router.post("/", status_code= status.HTTP_201_CREATED)
def create_posts(vote: schemas.Vote, db: Session = Depends(get_db), current_user: schemas.UserOut= Depends(oauth2.get_current_user)):

    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()

    if not post: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {vote.post_id} doesn't exist ")
    
    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id)

    vote_f = vote_query.first()

    if vote.dir == 1: 
        if vote_f: 
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"user: {current_user.id} has already voted on post: {vote.post_id}")
        
        vote_n = models.Vote(post_id= vote.post_id, user_id= current_user.id)
        db.add(vote_n)
        db.commit()

        return {"status": "successfully added vote"}

    else: 
        if not vote_f: 
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"user: {current_user.id} has not voted on post: {vote.post_id}")
        
        vote_query.delete(synchronize_session=False)
        db.commit()

        return {"status": "successfully deleted vote"}
      

