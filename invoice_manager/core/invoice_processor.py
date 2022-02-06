from datetime import datetime
from invoice_manager.models.invoice import Invoice
from invoice_manager.core.repository import InvoiceRepository


class PaymentProcessor:
    def __init__(self, repo: InvoiceRepository):
        self.repo = repo

    def pay_invoice(self, reference: str):
        invoice = self.repo.read_invoice(reference)
        invoice.pay()
        self.repo.update_invoice(invoice)

    def unpay_invoice(self, reference: str):
        invoice = self.repo.read_invoice(reference)
        invoice.unpay()
        self.repo.update_invoice(invoice)


class InvoiceCreator:
    def __init__(self, repo: InvoiceRepository):
        self.repo = repo

    def add_invoice(
        self, creation_date: str, issuer: str, nr: str, amount: float
    ) -> str:
        date = datetime.strptime(creation_date, "%Y-%m-%d")
        invoice = Invoice(creation_date=date, issuer=issuer, nr=nr, amount=amount)
        self.repo.create_invoice(invoice)
        return invoice.reference

    def delete_invoice(self, reference: str):
        self.repo.delete_invoice(reference)
