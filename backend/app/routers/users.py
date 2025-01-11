from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from sqlalchemy.orm import Session
from app.crud import user as crud_user
from app.schemas import user as schemas_user
from app.utils import dependencies, security
from app.utils.mongodb import get_database

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
router = APIRouter()

db = get_database()
posts_collection = db["posts"]


@router.post("/register", response_model=schemas_user.Token)
def register(user: schemas_user.UserCreate, db: Session = Depends(dependencies.get_db)):
    """
    Method used to register a new user

    Args:
        user (schemas_user.UserCreate): Form data containing user information
        db (Session, optional): Connector to the sqlite database. Defaults to Depends(dependencies.get_db).

    Raises:
        HTTPException: If the user can't be created, a 400 HTTP response will be sent

    Returns:
        dict: A dictionary containing the access_token and token_type
    """
    if crud_user.get_user(db, user.username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    db_user = crud_user.create_user(
        db, user.username, user.password)
    access_token = security.create_access_token(
        data={"username": db_user.username, "role": db_user.role})
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/profile")
def profile(token: str = Depends(oauth2_scheme),
            db: Session = Depends(dependencies.get_db)):
    """
    Method is used to return the profile information of a certain user

    Args:
        token (str, optional): The generated JWT token. Defaults to Depends(oauth2_scheme).
        db (Session, optional): Connector to the sqlite database. Defaults to Depends(dependencies.get_db).

    Raises:
        credentials_exception: If the token is invalid, a 401 HTTP response will be sent
        HTTPException: If the user is not found, a 404 HTTP response will be sent

    Returns:
        dict: The response contains user data, as well as the number of posts
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = security.decode_access_token(token)
        username = payload.get("username")
    except JWTError:
        raise credentials_exception

    user = crud_user.get_user(db, username)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    number_of_posts = posts_collection.count_documents({"author": username})

    response = {
        "user": user.as_dict(exclude="hashed_password"),
        "number_of_posts": number_of_posts
    }
    return response


@router.get("/all_users")
def get_users(token: str = Depends(oauth2_scheme),
              db: Session = Depends(dependencies.get_db)):
    """
    Method is used to get a list of all the users present in the database

    Args:
        token (str, optional): The generated JWT token. Defaults to Depends(oauth2_scheme).
        db (Session, optional): Connector to the sqlite database. Defaults to Depends(dependencies.get_db).

    Raises:
        HTTPException: If the user role is not admin, a 403 HTTP response will be sent
        credentials_exception: If the token is invalid, a 401 HTTP response will be sent

    Returns:
        list: A list contianing all the users
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = security.decode_access_token(token)
        current_user_role = payload.get("role")
        if current_user_role != "admin":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only admins can change user roles",
            )
    except JWTError:
        raise credentials_exception

    users = crud_user.get_users(db)
    return users


@router.put("/{username}/role")
def change_user_role(username: str, new_role: schemas_user.UserRoleUpdate, token: str = Depends(oauth2_scheme),
                     db: Session = Depends(dependencies.get_db)):
    """
    Method is used to change the role of a certain user

    Args:
        username (str): username whose role will be changed
        new_role (schemas_user.UserRoleUpdate): The form data will contain the new role
        token (str, optional): The generated JWT token. Defaults to Depends(oauth2_scheme).
        db (Session, optional): Connector to the sqlite database. Defaults to Depends(dependencies.get_db).

    Raises:
        HTTPException: If any error occurs, a certain HTTP error response will be sent
        credentials_exception: If the token is invalid, a 401 HTTP response will be sent

    Returns:
        dict: A success message
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = security.decode_access_token(token)
        current_user_role = payload.get("role")
        if current_user_role != "admin":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only admins can change user roles",
            )
    except JWTError:
        raise credentials_exception

    user = crud_user.get_user(db, username)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    user.role = new_role.role
    db.commit()
    return {"message": f"User '{username}' role changed to '{new_role.role}' successfully."}


@router.delete("/{username}")
def delete_user(username: str, token: str = Depends(oauth2_scheme),
                db: Session = Depends(dependencies.get_db)):
    """
    Method is used to delete a given user

    Args:
        username (str): username of the user that will be deleted
        token (str, optional): The generated JWT token. Defaults to Depends(oauth2_scheme).
        db (Session, optional): Connector to the sqlite database. Defaults to Depends(dependencies.get_db).

    Raises:
        HTTPException: If any error occurs, a certain HTTP error response will be sent
        credentials_exception: If the token is invalid, a 401 HTTP response will be sent

    Returns:
        dict: A success message
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = security.decode_access_token(token)
        current_user_role = payload.get("role")
        if current_user_role != "admin":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only admins can delete user accounts",
            )
    except JWTError:
        raise credentials_exception

    user = crud_user.get_user(db, username)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    posts_collection.delete_many({"author": username})

    crud_user.delete_user(db, user)

    return {"message": f"User '{username}' deleted successfully."}
