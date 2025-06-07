from models.base import Base
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime

class Category(Base):
    """
    Model reprezentujący kategorię słów lub gier.

    Atrybuty:
        id (int): Unikalny identyfikator kategorii.
        name (str): Nazwa kategorii (np. 'EASY', 'HARD').
    """
    __tablename__ = 'category'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
