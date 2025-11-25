from fastapi import APIRouter, Depends, HTTPException
from datetime import timedelta, datetime, timezone
from pydantic import BaseModel
from starlette import status
from models import Users
from passlib.context import CryptContext
from typing import Annotated
from sqlalchemy.orm import Session
from database import SessionLocal
from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
'''We're using OAuth2PasswordRequestForm. It's a special kind of form that will be slightly more secure and will 
have its own portal on Swagger. Where we will be able to get the username and password for the request. Now, once we 
import this request form, we now need to use it as a dependency injection for our API.'''

'''We're going to want to import OAuth2PasswordBearer. In the header of every API endpoint we're going to be passing 
in this bearer token, which is a JWT, and we're just telling fast API to check the bearer token in the header for this 
JWT before we process the request.'''

'''JWT is one of the most popular bearer tokens and authorization protocols within APIs'''


router = APIRouter(prefix="/auth", tags=["auth"])
'''Now API router will allow us to be able to route from our main.py file to our auth.py file.'''

SECRET_KEY = '4125c05a5588870941f58e133ef8a0734628a35f75f9a3e3096e9e70b4fcbd58'
ALGORITHM = 'HS256'
'''The secret and the algorithm will work together to add a signature to the JWT to make sure that JWT is secure 
and authorized.'''

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
'''It's just some setup information and default information that we need for our pathlib to work properly.'''

oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')
'''Now, this parameter (tokenUrl='token') contains the URL that the client will send to our fast API application. So 
we need this just to verify the token as a dependency in our API request.'''


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]


def authenticate_user(uname: str, pwd: str, db):
    user = db.query(Users).filter(Users.username == uname).first()
    if not user:
        return False
    if not bcrypt_context.verify(pwd, user.hashed_password):
        return False
    return user

def create_access_token(username: str, user_id: int, user_role: str, expires_delta: timedelta):
    encode = {'sub': username, 'id': user_id, 'role': user_role}
    expires = datetime.now(timezone.utc) + expires_delta
    encode.update({'exp': expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('sub')
        user_id: int = payload.get('id')
        user_role: str = payload.get('role')
        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate the user.')
        return {'username': username, 'id': user_id, 'user_role': user_role}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate the token.')


class CreateUserRequest(BaseModel):
    username: str
    email: str
    password: str
    first_name: str
    last_name: str
    role: str


class Token(BaseModel):
    access_token: str
    token_type: str


@router.post("/", status_code=status.HTTP_201_CREATED)
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


@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate the user.')
    token = create_access_token(user.username, user.id, user.role, timedelta(minutes=20))
    return {'access_token': token, 'token_type': 'bearer'}