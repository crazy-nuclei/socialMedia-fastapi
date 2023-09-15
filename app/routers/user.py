from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, utils
from ..database import get_db

router = APIRouter(prefix="/users", tags=["Users"])


@router.post('/',status_code= status.HTTP_201_CREATED ,response_model= schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):

    check_user = db.query(models.User).filter(models.User.email == user.email).first()

    if check_user: 
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"User with email: {user.email} already exists !")

    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    
    user = models.User(**user.model_dump())
    db.add(user)
    db.commit()
    db.refresh(user)

    return user


@router.get("/{id}", response_model= schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)): 
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user: 
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
                            detail= f"user with id: {id} does not exist")
    
    return user