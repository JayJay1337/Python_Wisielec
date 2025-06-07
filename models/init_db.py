import os
from sqlalchemy import create_engine
from models.base import Base
from models.session import DATABASE_URL
from models.user import User
from models.game_data import GameData
from models.category import Category
from models.word import Word

def init_db():
    """
    Inicjalizuje bazę danych tworząc katalog 'database' oraz wszystkie tabele
    zdefiniowane w modelach.

    Jeśli katalog 'database' nie istnieje, zostanie utworzony.
    Następnie tworzy silnik bazy i generuje tabele na podstawie metadanych modeli.
    """
    os.makedirs("database", exist_ok=True)
    engine = create_engine(DATABASE_URL, echo=True)
    Base.metadata.create_all(engine)