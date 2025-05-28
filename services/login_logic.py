from models.user import User

def login(username, password) -> bool:
    from models.session import SessionLocal
    session = SessionLocal()

    user = session.query(User).filter_by(username=username, password=password).first()
    session.close()

    if user is None:
        return False
    else:
        return True






