from typing import Union, TypedDict
import _shared
import datetime as dt


class Exam:
    id: int  # unsigned
    length: int
    alt: int
    minSize: int
    maxRooms: int
    average: int
    examCode: str
