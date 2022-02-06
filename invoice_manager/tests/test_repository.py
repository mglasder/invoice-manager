from datetime import datetime
import pytest
from invoice_manager.models.invoice import Invoice
from invoice_manager.core.repository import InvoiceMemoryRepository


@pytest.fixture
def repo():
    return InvoiceMemoryRepository()


@pytest.fixture
def invoice():
    invoice = Invoice(
        creation_date=datetime.strptime("2022-01-01", "%Y-%m-%d"),
        issuer="TestLab",
        nr="6001ABC",
        amount=302.15,
    )
    return invoice


def test_creating_invoice(repo, invoice):

    assert len(repo._invoices) == 0
    repo.create_invoice(invoice)
    assert len(repo._invoices) == 1


def test_reading_invoice(repo, invoice):
    ref = invoice.reference
    repo.create_invoice(invoice)
    inv = repo.read_invoice(reference=ref)
    assert invoice == inv


def test_updating_invoice(repo, invoice):
    ref = invoice.reference

    repo.create_invoice(invoice)
    inv = repo.read_invoice(reference=ref)
    assert invoice == inv
    assert invoice.is_paid is False

    inv.pay()
    repo.update_invoice(inv)

    new_inv = repo.read_invoice(reference=ref)
    assert new_inv.is_paid


def test_delete_invoice(repo, invoice):
    ref = invoice.reference
    repo.create_invoice(invoice)
    assert len(repo._invoices) == 1

    repo.delete_invoice(reference=ref)
    assert len(repo._invoices) == 0
