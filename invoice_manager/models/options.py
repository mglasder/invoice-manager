from enum import Enum

from invoice_manager.models.refundstatus import RefundStatus


class PaymentFilterOptions(Enum):
    any = "any"
    unpaid = "unpaid"
    paid = "paid"


class RefundFilterOptions(Enum):
    any = "any"
    open = "open"
    requested = "requested"
    confirmed = "confirmed"
    completed = "completed"
    declined = "declined"


class LogicalOperator(Enum):
    AND = "AND"
    OR = "OR"


class OptionsMapping:
    payment = {
        PaymentFilterOptions.any: None,
        PaymentFilterOptions.unpaid: False,
        PaymentFilterOptions.paid: True,
    }
    refund = {
        RefundFilterOptions.any: None,
        RefundFilterOptions.open: RefundStatus.OPEN,
        RefundFilterOptions.requested: RefundStatus.REQUESTED,
        RefundFilterOptions.confirmed: RefundStatus.CONFIRMED,
        RefundFilterOptions.completed: RefundStatus.DECLINED,
        RefundFilterOptions.declined: RefundStatus.COMPLETED,
    }
