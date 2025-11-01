from fastapi import FastAPI, Depends
import models
from database import engine, SessionLocal
from typing import Annotated
from sqlalchemy.orm import Session
from models import Todos

app = FastAPI()

models.Base.metadata.create_all(bind=engine)
'''models.Base.metadata.create_all(bind=engine) will create everything from our database.py file and our models.py 
file to be able to create a new database that has a new table of todos with all of the columns that we laid out in 
our models.py file. So this happens all behind the scenes. On how to create a new database for our fast API application 
using SQLite.'''

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

@app.get("/")
async def read_all(db: db_dependency):
    return db.query(Todos).all()

'''Depends is dependency injection. Dependency injection means in programming that we need to do something before 
we execute what we're trying to execute. And that will allow us to be able to do some kind of code behind the scenes 
and then inject the dependencies that function relies on.'''