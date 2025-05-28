from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from models.base import Base

class Game_Data(Base):
    __tablename__ = 'game_data'
    id = Column(Integer, primary_key=True)
    user_Id = Column(String, ForeignKey("user.id"))
    score = Column(Integer)
    game_date = Column(DateTime)
    category = Column(String(100))
    game_type = Column(String(100))
