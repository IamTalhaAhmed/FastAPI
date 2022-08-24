from datetime import datetime
from sqlalchemy.orm import Session

import models, schemas,hashing


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_user_name(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def get_by_date(db:Session,start_date:datetime,end_date:datetime):
    return db.query(models.Item).filter(models.Item.created_at>=start_date).filter(models.Item.created_at<=end_date).all()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = hashing.pwd_cxt.hash(user.password)
    db_user = models.User(username=user.username, password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Item).offset(skip).limit(limit).all()


def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int):
    db_item = models.Item(**item.dict(), owner_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item
