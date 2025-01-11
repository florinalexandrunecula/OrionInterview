from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from typing import List
from datetime import datetime
from bson.objectid import ObjectId
from backend.app.utils.mongodb import get_database
from backend.app.schemas.post import Post, PostUpdate
from backend.app.utils.security import SECRET_KEY, ALGORITHM

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

router = APIRouter()

db = get_database()
posts_collection = db["posts"]


def get_current_user(token: str = Depends(oauth2_scheme)):
    """
    Method will decode the given token and will extract the information it holds (username, role)

    Args:
        token (str, optional): The generated JWT token. Defaults to Depends(oauth2_scheme).

    Raises:
        HTTPException: If any errors occur, a corresponding HTTP Error will be raised

    Returns:
        dict: The decoded JWT data, in dictionary format
    """
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


def convert_post_obj(post: dict):
    """
    Method is mainly used to replace the data type of "_id" key from bson ObjectId format to str

    Args:
        post (dict): This is a forum post extracted from the MongoDB

    Returns:
        dict: The modified post dictionary
    """
    return {
        **post,
        "_id": str(post["_id"])
    }


@router.post("/posts")
def create_post(post: PostUpdate, current_user: dict = Depends(get_current_user)):
    """
    Method is used to create a post inside the forum

    Args:
        post (PostUpdate): The new post that will be saved inside the MongoDB
        current_user (dict, optional): The user making the request. Defaults to Depends(get_current_user).

    Raises:
        HTTPException: If the post can't be inserted inside the MongoDB, a 500 HTTP response will be sent

    Returns:
        dict: A success message
    """
    post_data = post.model_dump()
    post_data["author"] = current_user["username"]
    post_data["created_at"] = datetime.now()
    result = posts_collection.insert_one(post_data)
    if not result.inserted_id:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Post could not be created.")
    return {"message": "Post created successfully."}


@router.get("/posts", response_model=List[Post])
def get_posts(current_user: dict = Depends(get_current_user)):
    """
    Method will return all the posts for the forum

    Args:
        current_user (dict, optional): The user making the request. Defaults to Depends(get_current_user).

    Returns:
        List[Post]: A list of Post objects
    """
    posts = posts_collection.find()
    return [
        convert_post_obj(post)
        for post in posts
    ]


@router.get("/posts/{id}", response_model=Post)
def get_post(id: str, current_user: dict = Depends(get_current_user)):
    """
    Method will return the details of a certain post

    Args:
        id (str): id of the post
        current_user (dict, optional): The user making the request. Defaults to Depends(get_current_user).

    Raises:
        HTTPException: If the post is not found, a 404 HTTP response will be sent

    Returns:
        dict: The post data
    """
    post = posts_collection.find_one({"_id": ObjectId(id)})
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found.")
    return convert_post_obj(post)


@router.put("/posts/{id}")
def update_post(id: str, updated_post: PostUpdate, current_user: dict = Depends(get_current_user)):
    """
    Method is used to update a certain post

    Args:
        id (str): id of the post that will be updated
        updated_post (PostUpdate): The new post data
        current_user (dict, optional): The user making the request. Defaults to Depends(get_current_user).

    Raises:
        HTTPException: If any error occur, a corresponding HTTP Response will be sent

    Returns:
        dict: A success message
    """
    post = posts_collection.find_one({"_id": ObjectId(id)})
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
        {"_id": ObjectId(id)}, {"$set": updated_post})
    if result.modified_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Post not found or no changes made.")
    return {"message": "Post updated successfully."}


@router.delete("/posts/{id}")
def delete_post(id: str, current_user: dict = Depends(get_current_user)):
    """
    Method will delete a certain post

    Args:
        id (str): id of the post
        current_user (dict, optional): The user making the request. Defaults to Depends(get_current_user).

    Raises:
        HTTPException: If any error occur, a corresponding HTTP Response will be sent

    Returns:
        dict: A success message
    """
    post = posts_collection.find_one({"_id": ObjectId(id)})
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found.")

    if post["author"] != current_user["username"] and current_user["role"] != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="You do not have permission to delete this post.")

    result = posts_collection.delete_one({"_id": ObjectId(id)})
    if result.deleted_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found.")
    return {"message": "Post deleted successfully."}
