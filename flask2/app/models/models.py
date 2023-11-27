from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean
from .database import Base
from datetime import datetime


class OnegaiContent(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    name = Column(String(128), unique=True)
    body = Column(Text)
    date = Column(DateTime, default=datetime.now())
    # done = Column(Boolean, default=False, nullable=False)


    def __init__(self, name=None, body=None, date=None):
        self.name = name
        self.body = body
        self.date = date
        # self.done = done


    def __repr__(self):
        return '<Title %r>' % (self.title)