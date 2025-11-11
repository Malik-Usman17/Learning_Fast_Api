from fastapi import APIRouter, Depends
from pydantic import BaseModel
from starlette import status
from models import Users
from passlib.context import CryptContext
from typing import Annotated
from sqlalchemy.orm import Session
from database import SessionLocal


router = APIRouter()
'''Now API router will allow us to be able to route from our main.py file to our auth.py file.'''


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
'''It's just some setup information and default information that we need for our pathlib to work properly.'''

class CreateUserRequest(BaseModel):
    username: str
    email: str
    password: str
    first_name: str
    last_name: str
    role: str

@router.post("/auth", status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency, create_user_req: CreateUserRequest):
    create_user_model = Users(
        email = create_user_req.email,
        username = create_user_req.username,
        first_name = create_user_req.first_name,
        last_name = create_user_req.last_name,
        role = create_user_req.role,
        hashed_password = bcrypt_context.hash(create_user_req.password),
        is_active = True
    )

    db.add(create_user_model)
    db.commit()

    return create_user_model
