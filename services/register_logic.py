from models.user import User


def register(username, password, email):
    from models.session import SessionLocal
    session = SessionLocal()

    new_user = User(username=username, password=password, email=email)
    existing_user = session.query(User).filter_by(username=username).first()
    if existing_user:
        print("User already exists")
    else:
        session.add(new_user)
        session.commit()
    session.close()


