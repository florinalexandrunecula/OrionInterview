from sqlalchemy.orm import Session
from datetime import datetime
from app.utils.database import Base, engine
from app.models.user import User
from app.utils.security import get_password_hash
from app.utils.mongodb import client

Base.metadata.create_all(bind=engine)
DB_NAME = "forum"
COL_NAME = "posts"


def create_admin_user():
    """
    Function will populate the database with an admin user
    if no admin is present
    """
    db = Session(engine)
    if not db.query(User).filter(User.role == "admin").first():
        admin_user = User(
            username="admin",
            hashed_password=get_password_hash("adminpassword"),
            role="admin"
        )
        db.add(admin_user)
        db.commit()
        db.close()
        print("Admin user created successfully.")


def create_testing_user():
    """
    Function will populate the database with a testing user
    if no testing account is present
    """
    db = Session(engine)
    if not db.query(User).filter(User.username == "testuser").first():
        test_user = User(
            username="testuser",
            hashed_password=get_password_hash("password123"),
            role="user"
        )
        db.add(test_user)
        db.commit()
        db.close()
        print("Test user created successfully.")


def populate_mongodb():
    db = client[DB_NAME]
    col = db[COL_NAME]

    col.insert_one({
        "title": "Hello World!",
        "content": "This post was written automatically",
        "author": "admin",
        "created_at": datetime.now(),
        "updated_at": None
    })


create_admin_user()
create_testing_user()
populate_mongodb()
