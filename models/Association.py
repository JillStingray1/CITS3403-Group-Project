from sqlalchemy import  ForeignKey, Column, Table
from extensions import db, Base

association_table = Table(
    "association_table",
    db.Model.metadata,
    Column("user_id", ForeignKey("user.id"), primary_key=True),
    Column("meeting_id", ForeignKey("meeting.id"), primary_key=True),
)