from models.base import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship


class Word(Base):
    """
        Model reprezentujący słowo w bazie danych.

        Attributes:
            id (int): Unikalny identyfikator słowa.
            polish_word (str): Polskie słowo, które jest zgadywane w grze.
            category_id (int): Identyfikator kategorii, do której należy słowo (klucz obcy).
        """
    __tablename__ = 'word'

    id = Column(Integer, primary_key=True)
    polish_word = Column(String(200), nullable=False)
    category_id = Column(Integer, ForeignKey("category.id"), nullable=False)

