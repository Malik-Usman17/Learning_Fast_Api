from fastapi import FastAPI
import models
from database import engine
from routers import auth, todos, admin

app = FastAPI()

models.Base.metadata.create_all(bind=engine)
#because of this todos.db file created and whenever we have to change something in our model so
# we need to delete the todos.db file and run this function again.
# Also this models.Base.metadata.create_all(bind=engine) function will only run if todos.db does not exist.
'''models.Base.metadata.create_all(bind=engine) will create everything from our database.py file and our models.py 
file to be able to create a new database that has a new table of todos with all of the columns that we laid out in 
our models.py file. So this happens all behind the scenes. On how to create a new database for our fast API application 
using SQLite.'''

app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(admin.router)


#Username:malik12
#Pwd: malik123


#Username:Test_User1
#Pwd: User1234