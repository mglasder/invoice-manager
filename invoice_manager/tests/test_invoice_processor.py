from datetime import datetime
import pytest

from invoice_manager.core.invoice_processor import InvoiceCreator, PaymentProcessor
from invoice_manager.models.invoice import Invoice
from invoice_manager.core.repository import InvoiceMemoryRepository


@pytest.fixture
def repo():
    return InvoiceMemoryRepository()


@pytest.fixture
def creator(repo):
    return InvoiceCreator(repo)


@pytest.fixture
def payment_processor(repo):
    return PaymentProcessor(repo)


@pytest.fixture
def invoice():
    invoice = Invoice(
        creation_date=datetime.strptime("2022-01-01", "%Y-%m-%d"),
        issuer="TestLab",
        nr="6001ABC",
        amount=302.15,
    )
    return invoice


def test_add_invoice_adds_invoice_to_repo(creator, invoice):
    ref = invoice.reference

    assert len(creator.repo._invoices) == 0

    # TODO: Define test data properly, not via Invoice instance
    creator.add_invoice("2022-01-01", invoice.issuer, invoice.nr, invoice.amount)
    assert len(creator.repo._invoices) == 1

    assert creator.repo._invoices[0].reference == ref


def test_delete_invoice_deletes_invoice_from_repo(creator, invoice):
    creator.add_invoice("2022-01-01", invoice.issuer, invoice.nr, invoice.amount)
    assert len(creator.repo._invoices) == 1

    creator.delete_invoice(invoice.reference)
    assert len(creator.repo._invoices) == 0


def test_pay_invoice_pays_and_updates_invoice(creator, payment_processor, invoice):
    creator.add_invoice("2022-01-01", invoice.issuer, invoice.nr, invoice.amount)

    payment_processor.pay_invoice(invoice.reference)
    assert creator.repo._invoices[0].is_paid
