from sqlalchemy import Integer, String, ForeignKey, Column, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship, DeclarativeBase, validates
from extensions import db, Base
from models.Association import association_table

timeslot_length = [5, 10, 15, 20, 30, 60, 90, 120, 300] # in minutes

class Timeslot(db.Model):
    __tablename__ = 'timeslot'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    date: Mapped[Date] = mapped_column(Date, nullable=False)
    slot: Mapped[int] = mapped_column(Integer, nullable=False)
    selected: Mapped[int]   = mapped_column(Integer, nullable=False, default=0)# 0 = not selected and the slot is available. increment by one for each user who selects it as unavailable.
    meeting_id: Mapped[int] = mapped_column(ForeignKey("meeting.id"), nullable=False)

    

class Meeting(db.Model):
    __tablename__ = 'meeting'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    start_date: Mapped[Date] = mapped_column(Date, nullable=False)
    end_date: Mapped[Date] = mapped_column(Date, nullable=False)
    users: Mapped[list["user"]] = relationship(secondary=association_table, back_populates="meetings")
    meeting_length: Mapped[int] = mapped_column(Integer, nullable=False)
    meeting_name: Mapped[str] = mapped_column(String(80), nullable=False)
    meeting_description: Mapped[str] = mapped_column(String(2400), nullable=False)
    share_code: Mapped[str] = mapped_column(String(80), nullable=False)
    timeslots: Mapped[list["timeslot"]] = relationship()


    def __init__(self, start_date, end_date, **kwargs):
        if end_date < start_date:
            raise ValueError("end_date must be after or same as start_date")
        super().__init__(start_date=start_date, end_date=end_date, **kwargs)

    @validates("meeting_length")
    def validate_meeting_length(self, key, value):
        if value not in timeslot_length:
            raise ValueError(f"meeting_length must be one of {timeslot_length}")
        return value
    

        





