from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
"""
Konfiguracja połączenia z bazą danych SQLite oraz utworzenie sesji SQLAlchemy.
"""


DATABASE_URL = "sqlite:///database/userDatabase.db"

engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
