from sqlalchemy import Column, String, Integer, Boolean, ForeignKey
from database import Base

class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True)
    username = Column(String, unique=True)
    first_name = Column(String)
    last_name = Column(String)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    role = Column(String)
    contact_numb = Column(String)


class Todos(Base):
    __tablename__ = 'todos'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    priority = Column(Integer)
    complete = Column(Boolean, default=False)
    owner_id = Column(Integer, ForeignKey('users.id'))

'''index equals true means index is just a way for us to be able to increase performance by telling our database 
table that this is indexable, which means it's going to be unique. We're going to be able to find it directly and
it's just going to increase performance just slightly.'''



#$2b$12$MKA.V4bjHUsY2YbGU0zUCutBN4yor3IWHz6EqtpOU32ojcxY70Ec.