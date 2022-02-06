from invoice_manager.models.refundstatus import RefundStatus
from invoice_manager.core.repository import InvoiceRepository


class StatsCalculator:
    """The StatsCalculator is responsible for calculating statistics of the Invoice repo."""

    def __init__(self, repo: InvoiceRepository):
        self._repo = repo

    @property
    def _invoices(self):
        return self._repo.list_all()

    @property
    def payment_stats(self):
        stats = [self._calc_payment_status(ps=ps) for ps in [False, True]]
        return [self._calc_total()] + stats

    def _calc_total(self):
        return sum([inv.amount for inv in self._invoices])

    def _calc_payment_status(self, ps: bool):
        s = 0
        for inv in self._invoices:
            if inv.is_paid == ps:
                s += inv.amount
            else:
                s += 0.0
        return s

    @property
    def refund_stats(self):
        stats = [self._calc_refund_status(rs=rs) for rs in RefundStatus]
        return [sum(stats)] + stats

    def _calc_refund_status(self, rs: RefundStatus):
        s = 0
        for inv in self._invoices:
            if inv.refund_status == rs:
                s += inv.amount
            else:
                s += 0.0

        return s
