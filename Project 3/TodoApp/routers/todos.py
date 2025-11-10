from fastapi import FastAPI, APIRouter, Depends, HTTPException, Path, APIRouter
from starlette import status
from database import engine, SessionLocal
from typing import Annotated
from sqlalchemy.orm import Session
from models import Todos
from pydantic import BaseModel, Field
from routers import auth
import models

#app = FastAPI()
router = APIRouter()

models.Base.metadata.create_all(bind=engine)
#because of this todos.db file created and whenever we have to change something in our model so
# we need to delete the todos.db file and run this function again.
# Also this models.Base.metadata.create_all(bind=engine) function will only run if todos.db does not exist.
'''models.Base.metadata.create_all(bind=engine) will create everything from our database.py file and our models.py 
file to be able to create a new database that has a new table of todos with all of the columns that we laid out in 
our models.py file. So this happens all behind the scenes. On how to create a new database for our fast API application 
using SQLite.'''

app.include_router(auth.router)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
'''Now the yield means only the code prior to and including the yield statement is executed before sending a response. 
The code following the yield statement is executed after the response has been delivered. Now this makes fast API 
quicker because we can fetch information from a database, return it to the client and then close off the connection to
the database after. And it's extremely safe and pretty much required in most applications to open up a database 
connection only for when you're using the database and then close the connection after.'''


db_dependency = Annotated[Session, Depends(get_db)]


class TodoDataRequest(BaseModel):
    title: str = Field(min_length=3)
    description: str = Field(min_length=5, max_length=100)
    priority: int = Field(gt=0, lt=6)
    complete: bool


@app.get("/")
async def read_all(db: db_dependency):
    return db.query(Todos).all()
'''Depends is dependency injection. Dependency injection means in programming that we need to do something before 
we execute what we're trying to execute. And that will allow us to be able to do some kind of code behind the scenes 
and then inject the dependencies that function relies on.'''


@app.get("/todos/{requested_id}", status_code=status.HTTP_200_OK)
async def read_todo(db: db_dependency, requested_id: int = Path(gt=0)):
    todo_model = db.query(Todos).filter(Todos.id == requested_id).first()
    if todo_model is not None:
        return todo_model
    raise HTTPException(status_code=404, detail='Data not found!!')
'''Now to save some performance time, we can add another filter at the end is first(). The application 
doesn't know how many IDs have this path parameter ID within our todo table. Well, we know that this is the primary key 
and each is unique. So we want to say as soon as we get a match, we can return that data instead of looking through 
every single record in the database to see if the IDs match.'''


@app.post("/todos", status_code=status.HTTP_201_CREATED)
async def create_todo(db: db_dependency, todo_request: TodoDataRequest):
    todo_model = Todos(**todo_request.model_dump())
    db.add(todo_model)
    db.commit()
'''And then we're going to say DB dot add to do, which makes the session know that, hey, we're about to add something 
to this DB. The DB needs to know ahead of time what functionality is about to happen. And then we can finally say 
db.commit(), which will make this add functionality automatically happen to the database. So adding means getting the 
database ready while committing means flushing it all and actually doing the transaction to the database.'''


@app.put("/todos/{req_todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(
        db: db_dependency,
        todo_request: TodoDataRequest,
        req_todo_id: int = Path(gt=0)
):
    todo_data_model = db.query(Todos).filter(Todos.id == req_todo_id).first()
    if todo_data_model is None:
        raise HTTPException(status_code=404, detail='Todo Data not found!!')

    todo_data_model.title = todo_request.title
    todo_data_model.description = todo_request.description
    todo_data_model.priority = todo_request.priority
    todo_data_model.complete = todo_request.complete

    db.add(todo_data_model)
    db.commit()


@app.delete("/todos/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(db: db_dependency, todo_id: int = Path(gt=0)):
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail='Todo data not found.')
    db.query(Todos).filter(Todos.id == todo_id).delete()
    db.commit()

