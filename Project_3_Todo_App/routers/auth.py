from fastapi import APIRouter
'''Now API router will allow us to be able to route from our main.py file to our auth.py file.'''

router = APIRouter()

@router.get("/auth/")
async def get_user():
    return {"message": "Welcome to the Todos API!"}