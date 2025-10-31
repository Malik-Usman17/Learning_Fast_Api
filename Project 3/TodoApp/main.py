from fastapi import FastAPI
import models
from database import engine

app = FastAPI()

models.Base.metadata.create_all(bind=engine)
'''models.Base.metadata.create_all(bind=engine) will create everything from our database.py file and our models.py 
file to be able to create a new database that has a new table of to dos with all of the columns that we laid out in 
our models.py file. So this happens all behind the scenes. On how to create a new database for our fast API application 
using SQLite.'''