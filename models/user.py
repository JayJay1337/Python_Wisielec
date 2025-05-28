from sqlalchemy import Column, Integer, String, ForeignKey
from models.base import Base

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    Username = Column(String(100))
    Password = Column(String(100))
    Email = Column(String(100))
