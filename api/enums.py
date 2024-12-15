from enum import Enum


class DayOfWeek(str, Enum):
    MON = "Mon"
    TUE = "Tue"
    WED = "Wed"
    THUR = "Thur"
    FRI = "Fri"
    SAT = "Sat"
    SUN = "Sun"


class SortType(str, Enum):
    NAME = "name"
    PRICE = "price"