from sqlalchemy import Column, Integer, String, ForeignKey
from models.base import Base

class User(Base):
    """
    Model reprezentujący użytkownika w bazie danych.

    Attributes:
        id (int): Unikalny identyfikator użytkownika.
        username (str): Nazwa użytkownika.
        password (str): Zahashowane hasło użytkownika.
        email (str): Adres email użytkownika.
    """

    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String(100))
    password = Column(String(100))
    email = Column(String(100))
