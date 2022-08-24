from fastapi import APIRouter,Depends
from typing import List
import schemas,crud,database
from sqlalchemy.orm import Session

router = APIRouter()

@router.get("/users/", response_model=List[schemas.User],tags=['users'])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users

@router.post("/users/", response_model=schemas.User,tags=['users'])
def create_user(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    db_user = crud.get_user_by_user_name(db, username=user.username)
    if db_user:
        return "already registered"
    return crud.create_user(db=db, user=user)


@router.get("/users/{user_id}", response_model=schemas.User,tags=['users'])
def read_user(user_id: int, db: Session = Depends(database.get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        return "User not found"
    return db_user
