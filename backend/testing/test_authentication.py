import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from app.models.user import Base, User
from app.utils.security import get_password_hash
from app.routers.auth import login
from app.routers.users import register
from app.schemas.user import UserCreate


SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={
                       "check_same_thread": False})
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope="function", autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    hashed_password = get_password_hash("password123")
    db.add(User(username="testuser", hashed_password=hashed_password, role="user"))
    db.commit()
    db.close()
    yield
    Base.metadata.drop_all(bind=engine)


def test_login_success():
    form_data = OAuth2PasswordRequestForm(
        username="testuser", password="password123")
    db = next(override_get_db())
    response = login(form_data=form_data, db=db)
    assert "access_token" in response
    assert response["token_type"] == "bearer"


def test_login_invalid_password():
    form_data = OAuth2PasswordRequestForm(
        username="testuser", password="wrongpassword")
    db = next(override_get_db())
    with pytest.raises(Exception) as error:
        login(form_data=form_data, db=db)
    assert error.value.status_code == 401
    assert error.value.detail == "Invalid username or password"


def test_login_nonexistent_user():
    form_data = OAuth2PasswordRequestForm(
        username="nonexistentuser", password="password123")
    db = next(override_get_db())
    with pytest.raises(Exception) as error:
        login(form_data=form_data, db=db)
    assert error.value.status_code == 401
    assert error.value.detail == "Invalid username or password"


def test_register_success():
    db = next(override_get_db())
    new_user = UserCreate(username="newuser", password="password123")
    response = register(user=new_user, db=db)

    assert "access_token" in response
    assert response["token_type"] == "bearer"


def test_register_duplicate_user():
    db = next(override_get_db())
    duplicate_user = UserCreate(username="testuser", password="password123")

    with pytest.raises(HTTPException) as excinfo:
        register(user=duplicate_user, db=db)

    assert excinfo.value.status_code == 400
    assert excinfo.value.detail == "Username already registered"
