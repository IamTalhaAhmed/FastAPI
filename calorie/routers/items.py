from typing import List
import schemas,crud,database,models,oauth2
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime

router = APIRouter(
    prefix="/items",
    tags=["items"],
    responses={404: {"description": "Not found"}},
)

@router.get("/items/", response_model=List[schemas.Item])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db),current_user:schemas.User=Depends(oauth2.get_current_user)):
    items = crud.get_items(db, skip=skip, limit=limit)
    return items

@router.get('/get_items_by_date_range/{date_range}/',response_model=List[schemas.Item])
def get_by_date_range(s_date:datetime,e_date:datetime,db:Session=Depends(database.get_db)):
    items=crud.get_by_date(db,start_date=s_date,end_date=e_date)
    return items

@router.post("/users/{user_id}/items/", response_model=schemas.Item)
def create_item_for_user(
    user_id: int, item: schemas.ItemCreate, db: Session = Depends(database.get_db)
):
    return crud.create_user_item(db=db, item=item, user_id=user_id)

@router.put('/update_item/{name}')
def update_food(name:str,request:schemas.Item,db: Session = Depends(database.get_db)):
    food=db.query(models.Item).filter(models.Item.item_name == name).update(request.dict())
    db.commit()
    return food

@router.delete('/delete_food/{food_name}')
def delete_food(food_name:str,db: Session= Depends(database.get_db)):
    db.query(models.Item).filter(models.Item.item_name == food_name).delete(synchronize_session=False)
    db.commit()
    return {
        "message":"This item has been deleted successfully"
    }

