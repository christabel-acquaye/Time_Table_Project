import datetime as dt
from typing import TypedDict, Union

import _shared


class Exam:
    id: int  # unsigned
    length: int
    alt: int
    minSize: int
    maxRooms: int
    average: int
    examCode: str
