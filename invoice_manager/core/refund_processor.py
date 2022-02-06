from invoice_manager.models.exceptions import RefundStatusCannotChange
from invoice_manager.models.refundstatus import RefundStatus
from invoice_manager.core.repository import InvoiceRepository


class RefundProcessor:
    def __init__(self, repo: InvoiceRepository):
        self.repo = repo

    def request(self, reference: str):
        invoice = self.repo.read_invoice(reference)
        if invoice.refund_status == RefundStatus.OPEN:
            invoice.request_refund()
            self.repo.update_invoice(invoice)
            return invoice
        else:
            raise RefundStatusCannotChange(
                "Cannot change, because refund status is not OPEN. Consider rolling it back."
            )

    def confirm(self, reference: str):
        invoice = self.repo.read_invoice(reference)
        invoice.recieve_request_confirmation()
        self.repo.update_invoice(invoice)

    def decline(self, reference: str):
        invoice = self.repo.read_invoice(reference)
        invoice.recieve_request_decline()
        self.repo.update_invoice(invoice)

    def complete(self, reference: str):
        invoice = self.repo.read_invoice(reference)
        invoice.recieve_refund()
        self.repo.update_invoice(invoice)

    def rollback(self, reference: str):
        invoice = self.repo.read_invoice(reference)
        invoice.rollback_refund()
        self.repo.update_invoice(invoice)
