from enum import Enum


class RefundStatus(Enum):
    OPEN = "open"
    REQUESTED = "requested"
    CONFIRMED = "confirmed"
    DECLINED = "declined"
    COMPLETED = "completed"
