from sqlalchemy import  ForeignKey, Column, Table
from extensions import Base

association_table = Table(
    "association_table",
    Base.metadata,
    Column("user", ForeignKey("user.id")),
    Column("meeting", ForeignKey("meeting.id")),
)