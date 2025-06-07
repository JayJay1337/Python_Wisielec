from models.user import User
import bcrypt
import globals.user_id

def login(username, password):
    """
    Sprawdza poprawność danych logowania użytkownika.

    Pobiera użytkownika z bazy danych na podstawie nazwy użytkownika
    i porównuje podane hasło z zahashowanym hasłem w bazie danych
    za pomocą bcrypt.
    Przypisuje do zmiennej globalnej id użytkownika, który się zalogował.


    Args:
        username (str): Nazwa użytkownika.
        password (str): Hasło użytkownika w formie jawnej.

    Returns:
        bool: True jeśli dane logowania są poprawne, False w przeciwnym razie.
    """
    from models.session import SessionLocal
    session = SessionLocal()
    user = session.query(User).filter_by(username=username).first()
    globals.user_id.current_user=user.id
    session.close()

    if user and bcrypt.checkpw(password.encode(), user.password.encode()):
        return user
    else:
        return None
