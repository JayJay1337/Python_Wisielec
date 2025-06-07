from models.user import User
import bcrypt
import globals.user_id

def register(username, password, email):
    """
    Rejestruje nowego użytkownika.

    Hasło jest hashowane i zapisywane razem z nazwą użytkownika i e-mailem.
    Jeżeli użytkownik już istnieje, nie zostaje zarejestrowany.
    Przypisuje do zmiennej globalnej id użytkownika, który się zarejestrował.

    Args:
        username (str): Nazwa użytkownika.
        password (str): Hasło użytkownika (jawne).
        email (str): Adres e-mail użytkownika.
    """
    from models.session import SessionLocal
    session = SessionLocal()

    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    new_user = User(username=username, password=hashed_password.decode(), email=email)
    existing_user = session.query(User).filter_by(username=username).first()
    if existing_user:
        print("User already exists")
    else:
        session.add(new_user)
        session.commit()
        globals.user_id.current_user = new_user.id


