from sqlalchemy import  ForeignKey, Column, Table
from tools.extensions import db, Base

User_timeslot_association = Table(
    "User_timeslot_association",
    db.Model.metadata,
    Column("user_id", ForeignKey("user.id")),
    Column("timeslot_id", ForeignKey("timeslot.id")),
)
