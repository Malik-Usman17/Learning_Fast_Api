from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


SQLALCHEMY_DATABASE_URL = "sqlite:///./todos.db"

'''Well, we want to say check same thread of type false. And now by default, SQLite will only allow one thread to 
communicate with it.Assuming that each thread will handle an independent request. This is to prevent any kind of 
accident sharing of the same connection for different kind of requests. But in fast API it's very normal to have
more than one thread that could interact with the database at the same time. So we just need to make sure SQLite
knows that hey, we don't want to be checking the same thread all the time because there could be multiple threads 
happening to our SQLite database.'''
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})


'''So what we're saying is we want the session local, which we're going to be using in our application.
You'll see when we use session local, we want to bind to the engine that we just created and we want to 
make sure that our auto commits and auto flushes are false or the database transactions are going to try 
and do something automatically. And we want to be fully control of everything our database will do in the future.'''
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


'''So what we're saying here is later on, we want to be able to call our database.py file, be able to create 
a base which is an object of the database which is going to be able to then control our database. What this
really just means is we're going to be creating database tables and then here in our database.py we're 
going to be able to create an object of our database which will then be able to interact with the tables that we
create in the future.'''
Base = declarative_base()