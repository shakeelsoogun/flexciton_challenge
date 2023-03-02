from datetime import datetime
from typing import TypedDict


class CalendarEvent(TypedDict):
    name: str
    start_date: datetime
    end_date: datetime
