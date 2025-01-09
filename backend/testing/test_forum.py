import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from pymongo import MongoClient
from app.models.user import Base, User
from app.routers import forum
from app.schemas.post import PostUpdate
from app.utils.security import get_password_hash

MONGO_URL = "mongodb://localhost:27017"
TEST_DB_NAME = "forum_test"
client = MongoClient(MONGO_URL)
test_db = client[TEST_DB_NAME]
mock_posts_collection = test_db["posts"]

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
def setup_database(monkeypatch):
    monkeypatch.setattr(forum, "posts_collection", mock_posts_collection)

    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()

    hashed_password1 = get_password_hash("password123")
    hashed_password2 = get_password_hash("password456")
    db.add(User(username="testuser1", hashed_password=hashed_password1, role="user"))
    db.add(User(username="testuser2", hashed_password=hashed_password2, role="user"))
    db.commit()
    db.close()

    mock_posts_collection.delete_many({})

    yield

    Base.metadata.drop_all(bind=engine)
    mock_posts_collection.delete_many({})


def test_user1_create_edit_delete_post():
    current_user = {"username": "testuser1", "role": "user"}

    post_data = PostUpdate(title="My First Post",
                           content="This is my first post.")
    response = forum.create_post(post=post_data, current_user=current_user)
    assert response["message"] == "Post created successfully."

    posts = list(forum.get_posts(current_user=current_user))
    assert len(posts) == 1
    post_id = posts[0]["_id"]

    updated_post_data = PostUpdate(
        title="My Updated Post", content="Updated content.")
    update_response = forum.update_post(
        id=post_id, updated_post=updated_post_data, current_user=current_user)
    assert update_response["message"] == "Post updated successfully."

    delete_response = forum.delete_post(id=post_id, current_user=current_user)
    assert delete_response["message"] == "Post deleted successfully."


def test_user2_cannot_edit_or_delete_user1_post():
    user1 = {"username": "testuser1", "role": "user"}
    user2 = {"username": "testuser2", "role": "user"}

    post_data = PostUpdate(title="User1's Post",
                           content="This is user1's post.")
    forum.create_post(post=post_data, current_user=user1)

    posts = list(forum.get_posts(current_user=user1))
    assert len(posts) == 1
    post_id = posts[0]["_id"]

    updated_post_data = PostUpdate(
        title="Hacked Post", content="Hacked content.")
    with pytest.raises(Exception) as error:
        forum.update_post(
            id=post_id, updated_post=updated_post_data, current_user=user2)
    assert error.value.status_code == 403
    assert error.value.detail == "You do not have permission to edit this post."

    with pytest.raises(Exception) as error:
        forum.delete_post(id=post_id, current_user=user2)
    assert error.value.status_code == 403
    assert error.value.detail == "You do not have permission to delete this post."
