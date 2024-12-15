"""
This module contains enumeration classes used throughout the application.

"""

from enum import Enum


class DayOfWeek(str, Enum):
    """
    An enumeration representing the days of the week.
    """
    MON = "Mon"
    TUE = "Tue"
    WED = "Wed"
    THUR = "Thur"
    FRI = "Fri"
    SAT = "Sat"
    SUN = "Sun"


class SortType(str, Enum):
    """
    An enumeration representing sorting options.
    """
    NAME = "name"
    PRICE = "price"


class ComparisonType(str, Enum):
    """
    An enumeration representing comparison types.
    """
    MORE = "more"
    LESS = "less"


class SearchType(str, Enum):
    """
    An enumeration representing search types.
    """
    PHARMACY = "pharmacy"
    MASK = "mask"
    ALL = "all"
