from sqlalchemy import Column, String, Integer, Boolean
from database import Base


class Todos(Base):
    __tablename__ = 'todos'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    priority = Column(Integer)
    complete = Column(Boolean, default=False)

'''index equals true means index is just a way for us to be able to increase performance by telling our database 
table that this is indexable, which means it's going to be unique. We're going to be able to find it directly and
it's just going to increase performance just slightly.'''



