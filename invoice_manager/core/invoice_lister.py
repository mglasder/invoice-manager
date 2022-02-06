from typing import List, Union
import numpy as np
from invoice_manager.models.options import LogicalOperator
from invoice_manager.models.invoice import Invoice
from invoice_manager.models.refundstatus import RefundStatus


class InvoiceLister:
    """The Lister is responsible for filtering and listing the Invoice repo."""

    def __init__(self, repo):
        self._repo = repo

    @property
    def _invoices(self):
        return self._repo.list_all()

    def list_all(self) -> List[Invoice]:
        return self._invoices

    def filter_invoices(
        self,
        is_paid: Union[None, bool],
        refund_status: Union[None, RefundStatus],
        operator: LogicalOperator = LogicalOperator.AND,
    ) -> List[Invoice]:

        inv_ps = self._filter_payment_status(is_paid)
        inv_rs = self._filter_refund_status(refund_status)
        invoices = self._logical_combine(inv_ps, inv_rs, operator)
        return invoices

    def _filter_payment_status(self, is_paid: Union[None, bool]) -> List[Invoice]:
        if is_paid is None:
            return self._invoices

        return [inv for inv in self._invoices if inv.is_paid == is_paid]

    def _filter_refund_status(
        self, refund_status: Union[None, RefundStatus]
    ) -> List[Invoice]:
        if refund_status is None:
            return self._invoices

        return [inv for inv in self._invoices if inv.refund_status == refund_status]

    @staticmethod
    def _logical_combine(
        inv_ps: List[Invoice], inv_rs: List[Invoice], operator: LogicalOperator
    ) -> List[Invoice]:

        if operator == LogicalOperator.OR:
            return np.union1d(inv_ps, inv_rs).tolist()
        elif operator == LogicalOperator.AND:
            return np.intersect1d(inv_ps, inv_rs).tolist()
