from sqlalchemy.orm import Session
from app.utils.database import Base, engine
from app.models.user import User
from app.utils.security import get_password_hash

Base.metadata.create_all(bind=engine)


def create_admin_user():
    """
    Function will populate the database with an admin user
    if no admin is present
    """
    db = Session(engine)
    if not db.query(User).filter(User.role == "admin").first():
        admin_user = User(
            username="admin",
            hashed_password=get_password_hash("adminpassword"),
            role="admin"
        )
        db.add(admin_user)
        db.commit()
        db.close()
        print("Admin user created successfully.")


create_admin_user()
