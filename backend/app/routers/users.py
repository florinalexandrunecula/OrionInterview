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
        "user": user,
        "number_of_posts": number_of_posts
    }
    return response


@router.put("/users/{username}/role")
def change_user_role(username: str, new_role: str, token: str = Depends(oauth2_scheme),
                     db: Session = Depends(dependencies.get_db)):
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

    user.role = new_role
    db.commit()
    return {"message": f"User '{username}' role changed to '{new_role}' successfully."}
