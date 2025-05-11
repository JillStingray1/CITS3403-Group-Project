from tools import get_best_time_from_slot, format_meetings
from datetime import date, datetime
from models.Meeting import Meeting
import unittest


class TestMeetingTools(unittest.TestCase):
    def test_best_timeslot(self):
        # Testing calculation of best time from timeslot
        self.assertEqual(get_best_time_from_slot(0, date(2025, 5, 12)), datetime(2025, 5, 12, 9, 0))
        self.assertEqual(get_best_time_from_slot(32, date(2025, 5, 12)), datetime(2025, 5, 13, 9, 0))
        self.assertEqual(get_best_time_from_slot(67, date(2025, 5, 12)), datetime(2025, 5, 14, 9, 45))
        self.assertEqual(get_best_time_from_slot(121, date(2025, 5, 12)), datetime(2025, 5, 15, 15, 15))

    def test_format_meetings(self):
        future_year = 4000
        past_year = 2000
        # created meeting list to be sorted
        meetings = [
            Meeting(start_date=date(future_year, 5, 18), end_date=date(future_year + 1, 1, 1), best_timeslot=101),
            Meeting(start_date=date(future_year, 2, 11), end_date=date(future_year + 1, 1, 1), best_timeslot=20),
            Meeting(start_date=date(future_year, 7, 28), end_date=date(future_year + 1, 1, 1), best_timeslot=40),
            Meeting(start_date=date(past_year, 5, 18), end_date=date(past_year + 1, 1, 1), best_timeslot=101),
            Meeting(start_date=date(past_year, 2, 11), end_date=date(past_year + 1, 1, 1), best_timeslot=20),
            Meeting(start_date=date(past_year, 7, 28), end_date=date(past_year + 1, 1, 1), best_timeslot=40),
        ]
        # expected outputs
        expected_future_best_times = [
            datetime(future_year, 2, 11, 14, 0),
            datetime(future_year, 5, 21, 10, 15),
            datetime(future_year, 7, 29, 11),
        ]
        expected_past_best_times = [
            datetime(past_year, 7, 29, 11),
            datetime(past_year, 5, 21, 10, 15),
            datetime(past_year, 2, 11, 14),
        ]
        future_meetings, past_meetings = format_meetings(meetings)
        future_best_times = [meeting[0] for meeting in future_meetings]
        past_best_times = [meeting[0] for meeting in past_meetings]
        self.assertEqual(future_best_times, expected_future_best_times)
        self.assertEqual(past_best_times, expected_past_best_times)
