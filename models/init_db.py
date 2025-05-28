import os
from sqlalchemy import create_engine
from models.base import Base
from models.user import User
from models.game_data import Game_Data

if __name__ == "__main__":
    os.makedirs("database", exist_ok=True)
    engine = create_engine("sqlite:///database/userDatabase.db", echo=True)
    Base.metadata.create_all(engine)