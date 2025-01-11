from sqlalchemy import Column, Integer, String
from backend.app.utils.database import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, default="user")

    def as_dict(self, exclude=None):
        exclude = exclude or []
        return {key: value for key, value in self.__dict__.items() if key not in exclude and not key.startswith('_')}
