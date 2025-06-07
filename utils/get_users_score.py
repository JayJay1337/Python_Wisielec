from sqlalchemy.orm import Session
from models.user import User
from models.game_data import GameData

class UserDTO:
    """
    Data Transfer Object (DTO) dla wyników użytkownika.

    Atrybuty:
        username (str): Nazwa użytkownika.
        time (int): Wynik użytkownika (np. czas lub wynik punktowy).
        category_id (int): ID kategorii, w której uzyskano wynik.
    """
    def __init__(self, username, time, category_id):
        self.username = username
        self.time = time
        self.category_id = category_id


def get_users_score() -> list[UserDTO]:
    """
    Pobiera listę najlepszych 40 wyników użytkowników posortowanych rosnąco według wyniku.

    Łączy tabele User oraz GameData, pobierając nazwę użytkownika, wynik oraz kategorię gry.
    Wyniki są sortowane rosnąco (najlepsze wyniki na początku).

    Returns:
        list[UserDTO]: Lista obiektów UserDTO z danymi użytkowników i ich wynikami.
    """
    from models.session import SessionLocal
    session = SessionLocal()
    results = (
        session.query(User.username, GameData.time, GameData.category_id)
        .join(GameData, User.id == GameData.user_id)
        .order_by(GameData.time.asc())
        .limit(40)
        .all()
    )
    session.commit()
    session.close()
    return [UserDTO(username, time, category_id) for username, time, category_id in results]
