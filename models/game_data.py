from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from models.base import Base

class Game_Data(Base):
    __tablename__ = 'game_data'
    id = Column(Integer, primary_key=True)
    User_Id = Column(String, ForeignKey("user.id"))
    Score = Column(Integer)
    Game_Date = Column(DateTime)
    Category = Column(String(100))
    GameType = Column(String(100))
