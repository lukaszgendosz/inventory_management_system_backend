from enum import Enum


class Status(Enum):
    AVAILABLE = "available"
    CHECKED_OUT = "checked_out"
    RESERVERD = "reserved"
    BROKEN = "broken"
    LOST = "lost"
    ARCHIVED = "archived"
