from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from typing import List
from datetime import datetime
from app.utils.mongodb import get_database
from app.models.post import Post
from app.utils.security import SECRET_KEY, ALGORITHM

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

router = APIRouter()

db = get_database()
posts_collection = db["posts"]


def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("username")
        role = payload.get("role")
        if username is None or role is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return {"username": username, "role": role}
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


@router.post("/posts", response_model=Post)
def create_post(post: Post, current_user: dict = Depends(get_current_user)):
    post_data = post.model_dump()
    post_data["author"] = current_user["username"]
    result = posts_collection.insert_one(post_data)
    if not result.inserted_id:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Post could not be created.")
    return post


@router.get("/posts", response_model=List[Post])
def get_posts(current_user: dict = Depends(get_current_user)):
    return list(posts_collection.find({}, {"_id": 0}))


@router.get("/posts/{title}", response_model=Post)
def get_post(title: str, current_user: dict = Depends(get_current_user)):
    post = posts_collection.find_one({"title": title}, {"_id": 0})
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found.")
    return post


@router.put("/posts/{title}")
def update_post(title: str, updated_post: Post, current_user: dict = Depends(get_current_user)):
    post = posts_collection.find_one({"title": title})
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found.")

    if post["author"] != current_user["username"] and current_user["role"] != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="You do not have permission to edit this post.")

    updated_post = updated_post.model_dump()
    updated_post["updated_at"] = datetime.now()
    updated_post["author"] = post["author"]
    result = posts_collection.update_one(
        {"title": title}, {"$set": updated_post})
    if result.modified_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Post not found or no changes made.")
    return {"message": "Post updated successfully."}


@router.delete("/posts/{title}")
def delete_post(title: str, current_user: dict = Depends(get_current_user)):
    post = posts_collection.find_one({"title": title})
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found.")

    if post["author"] != current_user["username"] and current_user["role"] != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="You do not have permission to delete this post.")

    result = posts_collection.delete_one({"title": title})
    if result.deleted_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found.")
    return {"message": "Post deleted successfully."}
