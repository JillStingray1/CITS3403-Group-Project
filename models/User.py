from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from extensions import db
from models.Association import association_table



class User(db.Model):
    """
    Represents a registered user in the scheduling system.

    Each user has a unique username and a securely stored password hash.
    Users can be associated with multiple meetings through a many-to-many relationship.
    """
    __tablename__ = 'user'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(80), unique=True, nullable=False)

    # Hashed password string (e.g., bcrypt hash)
    password_hash: Mapped[str] = mapped_column(String(120), nullable=False)

    # Meetings this user is part of (many-to-many via association table)
    meetings: Mapped[list["meeting"]] = relationship(
        secondary=association_table,
        back_populates="users"
    )

    def __init__(self, username, password_hash, **kwargs):
        """
        Initializes a new User instance.
        
        Checks if the username is already taken and raises a ValueError if it is.
        Note: validate this in the route. This is just to avoid an error if bad data is passed.
        TODO: check if the username is valid once the functions have been implimented
        """
        existing = User.query.filter_by(username=username).first()
        if existing:
            raise ValueError(f"Username '{username}' already exists")
        
        super().__init__(username=username, password_hash=password_hash, **kwargs)