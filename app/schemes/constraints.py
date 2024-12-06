from enum import Enum


class Status(Enum):
    AVAILABLE = "available"
    DEPLOYED = "deployed"
    RESERVERD = "reserved"
    BROKEN = "broken"
    LOST = "lost"
    ARCHIVED = "archived"


class ExportType(Enum):
    CSV = "csv"


class EventType(Enum):
    CHECKOUT = "checkout"
    CHECKIN = "checkin"
    UPDATE = "update"
    CREATE = "create"
    DELETE = "delete"
