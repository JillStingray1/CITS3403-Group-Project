from sqlalchemy import Integer, String, ForeignKey, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship, DeclarativeBase
from extensions import db, Base
from models.Association import association_table

class Meeting(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    users: Mapped[list["User"]] = relationship(secondary=association_table, back_populates="meetings")
    