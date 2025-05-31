import os
from sqlalchemy import create_engine
from models.base import Base
from models.session import DATABASE_URL
from models.user import User
from models.game_data import GameData
from models.category import Category

def init_db():
    os.makedirs("database", exist_ok=True)
    engine = create_engine(DATABASE_URL, echo=True)
    Base.metadata.create_all(engine)