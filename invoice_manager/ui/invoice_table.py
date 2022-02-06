from typing import List
from prettytable import PrettyTable
from invoice_manager.models.invoice import Invoice


class InvoiceTable:
    def __init__(self):
        self._table = PrettyTable(
            [
                "REFERENCE",
                "DATE",
                "ISSUER",
                "NR",
                "AMOUNT [CHF]",
                "PAID",
                "REFUND STATUS",
            ]
        )

        self._format_table()

    def _format_table(self):
        self._table.align = "r"
        self._table.align["REFERENCE"] = "l"

    def create(self, invoices: List[Invoice], sort_by: str = "DATE") -> str:
        for inv in invoices:
            self._table.add_row(
                [
                    inv.reference,
                    str(inv.creation_date)[:11],
                    inv.issuer,
                    inv.nr,
                    f"{inv.amount:.2f}",
                    inv.is_paid,
                    inv.refund_status.value,
                ]
            )

        return self._table.get_string(sortby=sort_by)
