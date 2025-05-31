from models.base import Base
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
class GameData(Base):
    __tablename__ = 'game_data'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    score = Column(Integer)
    game_date = Column(DateTime)
    game_type = Column(String(100))
    category_id = Column(Integer, ForeignKey("category.id"))
