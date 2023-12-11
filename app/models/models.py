from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean
from .database import Base
from datetime import datetime


class OnegaiContent(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    name = Column(String(128), unique=True)
    body = Column(Text)
    date = Column(DateTime, default=datetime.now())
    done = Column(Boolean, default=False)


    def __init__(self, name=None, body=None, date=None, done=None):
        self.name = name
        self.body = body
        self.date = date
        self.done = done


    def __repr__(self):
        return '<Title %r>' % (self.name)
    

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    user_name = Column(String(128), unique=True)
    hashed_password = Column(String(128))

    def __init__(self, user_name=None, hashed_password=None):
        self.user_name = user_name
        self.hashed_password = hashed_password


    def __repr__(self):
        return '<Name %r>' % (self.user_name)