import datetime
from models.game_data import GameData

class GameDataDTO:
    """
    Data Transfer Object (DTO) dla danych gry.

    Atrybuty:
        user_id (int): ID użytkownika, który grał.
        Time (int): Czas gry.
        game_date (datetime.date): Data rozgrywki.
        category_id (int): ID kategorii gry.
    """
    def __init__(self, user_id, time, game_date, category_id):
        self.user_id = user_id
        self.time = time
        self.game_date = game_date
        self.category_id = category_id


def save_game_data(user_id, time, game_date, category_id):
    """
    Zapisuje dane gry do bazy danych.

    Tworzy obiekt GameData z podanymi parametrami i zapisuje go w bazie.

    Args:
        user_id (int): ID użytkownika.
        time (int): Czas gry.
        game_date (datetime.date): Data gry.
        category_id (int): ID kategorii gry.

    Raises:
        Exception: Przekazuje wyjątek w przypadku problemów z zapisem do bazy.

    """
    from models.session import SessionLocal
    session = SessionLocal()
    try:
        game_data = GameData(
            user_id=user_id,
            time=time,
            game_date=game_date,
            category_id=category_id
        )
        session.add(game_data)
        session.commit()
        session.refresh(game_data)

    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()
