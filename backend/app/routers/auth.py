from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.crud import user as crud_user
from app.utils import security, dependencies
from app.schemas import user as schemas_user

router = APIRouter()


@router.post("/login", response_model=schemas_user.Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(dependencies.get_db),
):
    """
    Route used to login the user

    Args:
        form_data (OAuth2PasswordRequestForm, optional): data received will contain username and password . Defaults to Depends().
        db (Session, optional): Connector to the sqlite database. Defaults to Depends(dependencies.get_db).

    Raises:
        HTTPException: If the username/password combination is invalid, a 401 HTTP Response will be sent

    Returns:
        dict: A dictionary containing the access_token and the token_type
    """
    user = crud_user.get_user(db, form_data.username)
    if not user or not security.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = security.create_access_token(
        data={"username": user.username,  "role": user.role})
    return {"access_token": access_token, "token_type": "bearer"}
