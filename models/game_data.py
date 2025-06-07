from models.base import Base
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, DECIMAL


class GameData(Base):
    """
    Model reprezentujący dane gry użytkownika.

    Atrybuty:
        id (int): Unikalny identyfikator rekordu.
        user_id (int): Identyfikator użytkownika (klucz obcy do tabeli 'user').
        time (Decimal): Czas w jakim użytkownik wygrał grę.
        game_date (datetime): Data i czas rozgrywki.
        category_id (int): Identyfikator kategorii (klucz obcy do tabeli 'category').
    """
    __tablename__ = 'game_data'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    time = Column(DECIMAL)
    game_date = Column(DateTime)
    category_id = Column(Integer, ForeignKey("category.id"))