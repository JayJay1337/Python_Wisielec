from models.base import Base
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime

class Category(Base):
    __tablename__ = 'category'
    id = Column(Integer, primary_key=True)
    name = Column(String)
