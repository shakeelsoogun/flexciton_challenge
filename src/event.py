from datetime import datetime
from typing import TypedDict


class Event(TypedDict):
    name: str
    start_date: datetime
    end_date: datetime

