from sqlalchemy.orm import Session
from datetime import datetime
from backend.app.utils.database import Base, engine
from backend.app.models.user import User
from backend.app.utils.security import get_password_hash
from backend.app.utils.mongodb import client

Base.metadata.create_all(bind=engine)


def create_admin_user(session: Session):
    """
    Populate the database with an admin user if none exists.
    """
    if not session.query(User).filter(User.role == "admin").first():
        admin_user = User(
            username="admin",
            hashed_password=get_password_hash("adminpassword"),
            role="admin"
        )
        session.add(admin_user)
        session.commit()
        print("Admin user created successfully.")


def create_testing_user(session: Session):
    """
    Populate the database with a testing user if none exists.
    """
    if not session.query(User).filter(User.username == "testuser").first():
        test_user = User(
            username="testuser",
            hashed_password=get_password_hash("password123"),
            role="user"
        )
        session.add(test_user)
        session.commit()
        print("Test user created successfully.")


def populate_mongodb():
    """
    Populate MongoDB with a sample post.
    """
    db = client["forum"]
    col = db["posts"]

    col.insert_one({
        "title": "Hello World!",
        "content": "This post was written automatically",
        "author": "admin",
        "created_at": datetime.now(),
        "updated_at": None
    })
    print("Sample post added to MongoDB.")


def main():
    with Session(engine) as session:
        create_admin_user(session)
        create_testing_user(session)

    populate_mongodb()
