from fastapi import APIRouter,Depends
import database,models,token_2
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from hashing import Hash
router= APIRouter(tags=['login'])

@router.post('/login')
def login(request:OAuth2PasswordRequestForm=Depends(),db:Session=Depends(database.get_db)):
    user=db.query(models.User).filter(models.User.username==request.username).first()
    if not user:
        return "invalid user"
    if not Hash.verify(user.password,request.passwrod):
        return "invalid user"

    access_token = token_2.create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}