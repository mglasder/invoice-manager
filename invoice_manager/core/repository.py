from abc import abstractmethod, ABCMeta
from typing import List

from invoice_manager.models.exceptions import (
    InvoiceNonexistent,
    InvoiceNotFound,
    InvoiceAlreadyExists,
)
from invoice_manager.models.invoice import Invoice


class InvoiceRepository(metaclass=ABCMeta):
    @abstractmethod
    def create_invoice(self, invoice: Invoice):
        raise NotImplementedError

    @abstractmethod
    def read_invoice(self, reference: str):
        raise NotImplementedError

    @abstractmethod
    def update_invoice(self, invoice: Invoice):
        raise NotImplementedError

    @abstractmethod
    def delete_invoice(self, reference: str):
        raise NotImplementedError

    @abstractmethod
    def list_all(self):
        raise NotImplementedError


class InvoiceMemoryRepository(InvoiceRepository):
    def __init__(self):
        self._invoices: List[Invoice] = []

    def create_invoice(self, invoice: Invoice):
        if invoice in self._invoices:
            raise InvoiceAlreadyExists
        else:
            self._invoices.append(invoice)

    def read_invoice(self, reference: str) -> Invoice:
        for invoice in self._invoices:
            if invoice.reference == reference:
                return invoice

        raise InvoiceNotFound

    def update_invoice(self, invoice: Invoice):
        ref = invoice.reference
        self.delete_invoice(ref)
        self.create_invoice(invoice)

    def delete_invoice(self, reference: str):
        for i, invoice in enumerate(self._invoices):
            if invoice.reference == reference:
                del self._invoices[i]
                return

        raise InvoiceNonexistent

    def list_all(self) -> List[Invoice]:
        return self._invoices
