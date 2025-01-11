from fastapi import FastAPI
from backend.app.routers import auth, users, forum

app = FastAPI()

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(forum.router, prefix="/forum", tags=["forum"])
