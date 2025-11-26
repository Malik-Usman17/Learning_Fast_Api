from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from starlette import status
from models import Users
from passlib.context import CryptContext
from typing import Annotated
from sqlalchemy.orm import Session
from database import SessionLocal
from routers.auth import get_current_user

router = APIRouter(prefix="/users", tags=["users_list"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserVerification(BaseModel):
    old_password: str
    new_password: str = Field(min_length=6)


@router.get("/userInfo", status_code=status.HTTP_200_OK)
async def get_user_info(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication failed sorry.")
    return db.query(Users).filter(Users.id == user.get('id')).first()


@router.put("/update_password", status_code=status.HTTP_204_NO_CONTENT)
async def update_password(user: user_dependency, db: db_dependency, user_verification: UserVerification):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication failed, please check again.")
    user_model = db.query(Users).filter(Users.id == user.get('id')).first()
    if not bcrypt_context.verify(user_verification.old_password, user_model.hashed_password):
        raise HTTPException(status_code=401, detail="Error on password change.")
    '''if len(user_verification.new_password) < 6:
        raise HTTPException(status_code=422, detail="Password length should be at least 6 characters.")'''
    user_model.hashed_password = bcrypt_context.hash(user_verification.new_password)
    db.add(user_model)
    db.commit()



'''
    if len(user_verification.new_password) < 6:
        raise HTTPException(status_code=422, detail="Password length should be at least 6 characters.")
above line of code is not running because, I'm mentioning the pydantic validation in UserVerification and the concept 
is FastAPI runs Pydantic validation before your endpoint function is executed.
If new_password has length < 6, Pydantic raises a validation error.
FastAPI converts that into a 422 Unprocessable Entity with its own auto-generated error body.
Because validation failed, update_password(...) is never called.
'''