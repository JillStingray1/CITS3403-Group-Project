from sqlalchemy import Integer, String, ForeignKey, Column, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship, DeclarativeBase
from extensions import db, Base
from models.Association import association_table


class User(db.Model):
    __tablename__ = 'user'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(80), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(120), nullable=False)
    meetings: Mapped[list["meeting"]] = relationship(secondary=association_table, back_populates="users")
