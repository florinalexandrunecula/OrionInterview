from pydantic import BaseModel


class UserCreate(BaseModel):
    username: str
    password: str
    role: str = "user"


class UserRoleUpdate(BaseModel):
    role: str


class Token(BaseModel):
    access_token: str
    token_type: str
