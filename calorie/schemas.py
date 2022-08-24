from pydantic import BaseModel
from datetime import datetime

class ItemBase(BaseModel):
    calories: int
    created_at: datetime | None = None
    item_name:str


class ItemCreate(ItemBase):
    pass


class Item(ItemBase):
    item_name: str
    owner_id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    username : str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    items: list[Item] = []

    class Config:
        orm_mode = True

class login(BaseModel):
    username:str
    passwrod:str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None