
from sqlalchemy import Integer, String, ForeignKey, Column, Table
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
  pass

association_table = Table(
    "association_table",
    Base.metadata,
    Column("user", ForeignKey("user.id")),
    Column("meeting", ForeignKey("meeting.id")),
)

db = SQLAlchemy(model_class=Base)