from sqlalchemy import Column, Integer, String, ForeignKey
from models.base import Base

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String(100))
    password = Column(String(100))
    email = Column(String(100))
