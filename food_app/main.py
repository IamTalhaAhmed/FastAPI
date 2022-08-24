from lib2to3.pytree import Base
from unicodedata import name
import databases,sqlalchemy,datetime
from datetime import datetime
from fastapi import FastAPI
from sqlalchemy import create_engine,ForeignKey,Column, Integer, String
from sqlalchemy.orm import relationship
from pydantic import BaseModel,Field
from typing import List,Optional,Generic, TypeVar

#connecting to a database


DATABASE_URL='postgresql://admin:admin123@127.0.0.1:5000/calorie-db'
database=databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()

#creating a table (models)

class Item(Base):
    __tablename__ = "items"
    name= Column(String, primary_key=True)
    calories = Column(Integer)
    date = Column(String)
    creator=relationship("User",back_populates='items')
    user_id = Column(Integer, ForeignKey("users.id"))


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    password = Column(String)
    name=Column(String)
    items = relationship("Item", back_populates="creator")


#ceating an engine


engine = create_engine(DATABASE_URL)
metadata.create_all(engine)


class food_list(BaseModel):
    name: str
    calories:int
    date:str

    class Config:
        orm_mode = True

class food_entry(BaseModel):
    name:str=Field(..., example='abc')
    calories:int=Field(..., example=5)
    date:str=Field(...,example='dd/mm/yy')

class food_update(BaseModel):
    name:str=Field(...,example='Enter food name')
    calories:int=Field(..., example=5)
    date:str=Field(..., example='xyz')

class food_delete(BaseModel):
    name:str=Field(...,example='Enter food name')

class create_users(BaseModel):
    id : int
    name : str
    password : str

class filter_food(BaseModel):
    start_date:str=Field(...,example='mm/dd/yy')
#app


app=FastAPI()

#functions and decorators


@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

@app.get('/food',response_model=List[food_list],tags=['food'])
async def find_all_foods():
    query =foods.select()
    return await database.fetch_all(query)


@app.post('/food',response_model=food_list,tags=['food'])
async def register_food(food: food_entry):
    query=foods.insert().values(
        name=food.name,
        calories=food.calories,
        date=food.date
    )

    await database.execute(query)
    return{
        **food.dict()
    }

@app.get("/food_name/{food_name}",response_model=food_list,tags=['food'])
async def find_food_by_name(food_name:str):
    query=foods.select().where(foods.c.name == food_name)
    return await database.fetch_one(query)

@app.put('/food',response_model=food_list,tags=['food'])
async def update_food(food:food_update):
    query=foods.update().\
        where(foods.c.name==food.name).\
            values(
                name=food.name,
                calories=food.calories,
                date= food.date
            )
    await database.execute(query)

    return await find_food_by_name(food.name)

@app.delete('/food/{food_name}',tags=['food'])
async def delete_food(food:food_delete):
    query=foods.delete().where(foods.c.name==food.name)
    await database.execute(query)

    return {
        "message":"This item has been deleted successfully"
    }

@app.get('/food_date/{date_range}',response_model=List[food_list],tags=['food'])
async def filtered_food_item(start_date:str,end_date:str):
    query=foods.select().where( foods.c.date >= start_date ).where(foods.c.date<= end_date)
    return await database.fetch_all(query)

@app.post('/user',tags=['users'])
async def create_user(request: create_users):
    new_user = users.insert().values(
        id = request.id,
        name=request.name,
        password=request.password
    )

    await database.execute(new_user)
    return{

        **request.dict()
    }



























