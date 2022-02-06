import hashlib
from datetime import datetime
from pydantic import BaseModel

from invoice_manager.models.refundstatus import RefundStatus


class Invoice(BaseModel):
    creation_date: datetime
    issuer: str
    nr: str
    amount: float
    is_paid: bool = False
    refund_status: RefundStatus = RefundStatus.OPEN

    def __hash__(self):
        return hashlib.sha256(bytes(f"{self.nr}{self.issuer}", "UTF-8")).hexdigest()

    @property
    def reference(self):
        return self.__hash__()[:8]

    @property
    def filedate(self):
        return datetime.strftime(self.creation_date, "%y%m%d")

    @property
    def shortdate(self):
        return datetime.strftime(self.creation_date, "%Y-%m-%d")

    @property
    def filename(self):
        return f"{self.filedate}_{self.issuer}_{self.nr}_{self.amount:.2f}.pdf"

    def __lt__(self, other):
        return tuple(self.dict().values()) < tuple(other.dict().values())

    def __le__(self, other):
        return tuple(self.dict().values()) <= tuple(other.dict().values())

    def __gt__(self, other):
        return tuple(self.dict().values()) > tuple(other.dict().values())

    def __ge__(self, other):
        return tuple(self.dict().values()) >= tuple(other.dict().values())

    def pay(self):
        self.is_paid = True

    def unpay(self):
        self.is_paid = False

    def request_refund(self):
        self.refund_status = RefundStatus.REQUESTED

    def recieve_request_confirmation(self):
        self.refund_status = RefundStatus.CONFIRMED

    def recieve_request_decline(self):
        self.refund_status = RefundStatus.DECLINED

    def recieve_refund(self):
        self.refund_status = RefundStatus.COMPLETED

    def rollback_refund(self):
        self.refund_status = RefundStatus.OPEN
