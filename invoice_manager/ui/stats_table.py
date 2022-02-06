from typing import List, Tuple
from prettytable import PrettyTable
from invoice_manager.models.invoice import Invoice


class StatsTable:
    def __init__(self):
        self._payment = PrettyTable(["TOTAL", "UNPAID", "PAID"])
        self._refund = PrettyTable(
            ["SUM", "OPEN", "REQUESTED", "CONFIRMED", "DECLINED", "COMPLETED"]
        )

        self._format_table()

    def _format_table(self):
        self._payment.align = "r"
        self._payment.align["TOTAL"] = "l"
        self._refund.align = "r"
        self._refund.align["SUM"] = "l"

    @staticmethod
    def _create_table(table: PrettyTable, stats: List[float]) -> str:
        table.add_row([f"{s:.2f} CHF" for s in stats])
        return table.get_string()

    def create(
        self, payment_stats: List[float], refund_stats: List[float]
    ) -> Tuple[str, str]:
        payment_tab = self._create_table(self._payment, payment_stats)
        refund_tab = self._create_table(self._refund, refund_stats)
        return payment_tab, refund_tab
