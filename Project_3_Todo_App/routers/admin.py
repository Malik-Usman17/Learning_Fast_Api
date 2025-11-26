from fastapi import Depends, HTTPException, Path, APIRouter
from starlette import status
from database import SessionLocal
from typing import Annotated
from sqlalchemy.orm import Session
from models import Todos
from .auth import get_current_user


router = APIRouter(prefix="/company_admin", tags=["admin"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


@router.get("/todos", status_code=status.HTTP_200_OK)
async def read_all_todos(user: user_dependency, db: db_dependency):
    if user is None or user.get('user_role') != "admin":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="!!!!Unauthorized!!!!")
    return db.query(Todos).all()

@router.delete("/todos/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(user_dp: user_dependency, db: db_dependency, todo_id: int = Path(gt=0)):
    if user_dp is None or user_dp.get('user_role') != "admin":
        raise HTTPException(status_code=401, detail="!!!!Unauthorized!!!!")
    todos = db.query(Todos).filter(Todos.id == todo_id).first()
    if todos is None:
        raise HTTPException(status_code=404, detail='Sorry, todo data is not found')
    db.query(Todos).filter(Todos.id == todo_id).delete()
    db.commit()