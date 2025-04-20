from sqlalchemy import Integer, String, ForeignKey, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates
from extensions import db
from models.Association import association_table

timeslot_length = [5, 10, 15, 20, 30, 60, 90, 120, 300] # in minutes

class Timeslot(db.Model):
    """
    Represents a single selectable time slot for a meeting.

    Each timeslot is tied to a specific date and slot number (e.g., a division of the day).
    The `selected` field tracks how many users have marked this slot as unavailable.
    """
    __tablename__ = 'timeslot'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    date: Mapped[Date] = mapped_column(Date, nullable=False)
    slot: Mapped[int] = mapped_column(Integer, nullable=False)
    
    # Number of users who have marked this slot as unavailable.
    # 0 = available. Each additional user increments this by 1.
    selected: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    # Foreign key to the associated meeting
    meeting_id: Mapped[int] = mapped_column(ForeignKey("meeting.id"), nullable=False)

    def increment(self):
        """Increment the selected value by 1"""
        step = 1
        self._selected += step

    def decrement(self):
        """Decrement the selected value by 1"""
        step = 1
        self._selected -= step

    @property
    def selected(self):
        """Read-only access to selected."""
        return self._selected

    @selected.setter
    def selected(self, value):
        raise AttributeError("Direct modification of 'selected' is not allowed. Use increment() or decrement().")

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
    users: Mapped[list["user"]] = relationship(
        secondary=association_table, back_populates="meetings"
    )
    meeting_length: Mapped[int] = mapped_column(Integer, nullable=False)
    meeting_name: Mapped[str] = mapped_column(String(80), nullable=False)
    meeting_description: Mapped[str] = mapped_column(String(2400), nullable=True)

    # Public-facing share code to invite others to this meeting
    share_code: Mapped[str] = mapped_column(String(80), nullable=False)

    # List of all timeslots associated with this meeting
    timeslots: Mapped[list["timeslot"]] = relationship()

    def __init__(self, start_date, end_date, **kwargs):
        """
        Ensures that the end date is not before the start date when creating a meeting.
        """
        if end_date < start_date:
            raise ValueError("end_date must be after or same as start_date")
        super().__init__(start_date=start_date, end_date=end_date, **kwargs)

    @validates("meeting_length")
    def validate_meeting_length(self, key, value):
        """
        Validates that the meeting length is one of the allowed slot lengths.
        `timeslot_length` is assumed to be a predefined list of valid durations.
        """
        if value not in timeslot_length:
            raise ValueError(f"meeting_length must be one of {timeslot_length}")
        return value


