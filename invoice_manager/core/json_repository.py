import json
import os
from pathlib import Path
from typing import List

from invoice_manager.models.invoice import Invoice
from invoice_manager.core.repository import (
    InvoiceRepository,
)
from invoice_manager.models.exceptions import (
    InvoiceNonexistent,
    InvoiceNotFound,
    InvoiceAlreadyExists,
)


class InvoiceJsonRepository(InvoiceRepository):
    def __init__(self, repo_path: Path):
        self._repo_path = repo_path
        self._init_repo()

    @property
    def _invoices(self) -> List[Invoice]:
        with self._repo_path.open("r") as f:
            invoices = json.load(f)
        return [Invoice(**json.loads(inv)) for inv in invoices]

    def _init_repo(self):
        os.makedirs(os.path.dirname(self._repo_path), exist_ok=True)
        if not os.path.isfile(self._repo_path):
            with self._repo_path.open("w") as f:
                json.dump([], f)

    def _dump_invoices(self, invoices: List[Invoice]):
        invoices_new = [inv.json() for inv in invoices]
        with self._repo_path.open("w") as f:
            json.dump(invoices_new, f)

    def create_invoice(self, invoice: Invoice):
        invoices = self._invoices
        if invoice in invoices:
            raise InvoiceAlreadyExists(invoice.reference)
        else:
            invoices.append(invoice)
            self._dump_invoices(invoices)

    def read_invoice(self, reference: str) -> Invoice:
        for invoice in self._invoices:
            if invoice.reference == reference:
                return invoice

        raise InvoiceNotFound

    def update_invoice(self, invoice: Invoice):
        self.delete_invoice(invoice.reference)
        self.create_invoice(invoice)

    def delete_invoice(self, reference: str):
        invoices = self._invoices

        idx = None
        for i, invoice in enumerate(invoices):
            if invoice.reference == reference:
                idx = i
                break
        if idx is not None:
            del invoices[idx]
            self._dump_invoices(invoices)
        else:
            raise InvoiceNonexistent

    def list_all(self) -> List[Invoice]:
        return self._invoices
