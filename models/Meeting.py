from sqlalchemy import Integer, String, ForeignKey, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates
from extensions import db
from models.Association import association_table
from models.User_timeslot import User_timeslot_association

timeslot_length = [15, 30, 45, 60, 90, 120, 300] # in minutes

class Timeslot(db.Model):
    """
    Represents a single selectable time slot for a meeting.

    Each timeslot is tied to a specific meeting (e.g., a division of the day).
    The `selected` field tracks how many users have marked this slot as unavailable.
    """
    __tablename__ = 'timeslot'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    order: Mapped[int] = mapped_column(Integer, nullable=False)
    
    unavailable_users: Mapped[list['User']] = relationship("User",
        secondary=User_timeslot_association,
        backref="users")

    # Foreign key to the associated meeting
    meeting_id: Mapped[int] = mapped_column(ForeignKey("meeting.id"), nullable=False)



class Meeting(db.Model):
    """
    Represents a meeting that users can vote on for scheduling.

    Includes a shareable code, the preferred date range, and duration (in slots).
    Users can be associated with the meeting through a many-to-many relationship.
    """
    __tablename__ = 'meeting'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    start_date: Mapped[Date] = mapped_column(Date, nullable=False)
    end_date: Mapped[Date] = mapped_column(Date, nullable=False)
    
    # Users linked to the meeting (many-to-many)
    users: Mapped[list["User"]] = relationship("User",
        secondary=association_table,
        back_populates="meetings"
    )
    meeting_length: Mapped[int] = mapped_column(Integer, nullable=False)
    meeting_name: Mapped[str] = mapped_column(String(80), nullable=False)
    meeting_description: Mapped[str] = mapped_column(String(2400), nullable=True)

    # Public-facing share code to invite others to this meeting
    share_code: Mapped[str] = mapped_column(String(80), nullable=False)

    # List of all timeslots associated with this meeting
    timeslots: Mapped[list["Timeslot"]] = relationship()

    def __init__(self, start_date, end_date, **kwargs):
        """
        Ensures that the end date is not before the start date when creating a meeting.
        """
        if end_date < start_date:
            raise ValueError("end_date must be after or same as start_date")
        super().__init__(start_date=start_date, end_date=end_date, **kwargs)

    @validates("meeting_length")
    def validate_meeting_length(self, value):
        """
        Validates that the meeting length is one of the allowed slot lengths.
        `timeslot_length` is assumed to be a predefined list of valid durations.
        """
        if value not in timeslot_length:
            raise ValueError(f"meeting_length must be one of {timeslot_length}")
        return value


