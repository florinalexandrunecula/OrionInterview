import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.crud.user import get_user, get_users, create_user, delete_user
from app.models.user import Base, User
from app.utils.security import verify_password

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={
                       "check_same_thread": False})

TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


def test_create_user(db):
    username = "testuser"
    password = "password123"
    user = create_user(db, username, password)

    assert user.username == username
    assert verify_password(password, user.hashed_password)


def test_get_user(db):
    username = "testuser"
    password = "password123"
    create_user(db, username, password)

    user = get_user(db, username)

    assert user is not None
    assert user.username == username


def test_get_users(db):
    create_user(db, "user1", "password1")
    create_user(db, "user2", "password2")

    users = get_users(db)

    assert len(users) == 2
    assert users[0].username == "user1"
    assert users[1].username == "user2"


def test_delete_user(db):
    user = create_user(db, "testuser", "password123")

    result = delete_user(db, user)

    assert result is True
    assert get_user(db, "testuser") is None


def test_create_duplicate_user(db):
    username = "testuser"
    password = "password123"

    create_user(db, username, password)

    with pytest.raises(Exception) as error:
        create_user(db, username, password)

    assert "UNIQUE constraint failed" in str(error.value)
