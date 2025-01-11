from sqlalchemy.orm import Session
from backend.app.models.user import User
from backend.app.utils.security import get_password_hash


def get_user(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()






def get_users(db: Session):
    return db.query(User).all()


def delete_user(db: Session, user: User):
    try:
        db.delete(user)
        db.commit()
    except Exception as e:
        print("Caught following exception: {e}")
        return False
    return True


def create_user(db: Session, username: str, password: str):
    hashed_password = get_password_hash(password)
    db_user = User(username=username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
