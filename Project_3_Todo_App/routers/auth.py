from fastapi import APIRouter
from pydantic import BaseModel
from models import Users
from passlib.context import CryptContext


'''Now API router will allow us to be able to route from our main.py file to our auth.py file.'''

router = APIRouter()

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
'''It's just some setup information and default information that we need for our pathlib to work properly.'''

class CreateUserRequest(BaseModel):
    username: str
    email: str
    password: str
    first_name: str
    last_name: str
    role: str

@router.post("/auth/")
async def get_user(create_user_req: CreateUserRequest):
    create_user_model = Users(
        email = create_user_req.email,
        username = create_user_req.username,
        first_name = create_user_req.first_name,
        last_name = create_user_req.last_name,
        role = create_user_req.role,
        hashed_password = bcrypt_context.hash(create_user_req.password),
        is_active = True
    )

    return create_user_model
    return {"message": "Welcome to the Todos API!"}