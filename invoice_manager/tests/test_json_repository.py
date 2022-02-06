import json
import os
from datetime import datetime
import pytest

from invoice_manager.core.json_repository import InvoiceJsonRepository
from invoice_manager.models.invoice import Invoice


@pytest.fixture
def invoice1():
    invoice = Invoice(
        creation_date=datetime.strptime("2022-01-01", "%Y-%m-%d"),
        issuer="JSONLab",
        nr="101",
        amount=123.45,
    )
    return invoice


@pytest.fixture
def invoice2():
    invoice = Invoice(
        creation_date=datetime.strptime("2022-02-02", "%Y-%m-%d"),
        issuer="JSONLab",
        nr="202",
        amount=678.90,
    )
    return invoice


@pytest.fixture
def mock_json_repo_file(tmp_path):
    repo_path = tmp_path / "invoices.json"
    # with repo_path.open("w") as repo_file:
    #     json.dump(invoice, repo_file)
    return repo_path


@pytest.fixture
def json_repo(mock_json_repo_file):
    return InvoiceJsonRepository(mock_json_repo_file)


def test_init_of_json_repo(mock_json_repo_file):
    repo = InvoiceJsonRepository(mock_json_repo_file)
    with repo._repo_path.open("r") as f:
        assert json.load(f) == []


def test_create_invoice_in_json_repo_creates_json_dump(json_repo, invoice1):
    json_repo.create_invoice(invoice1)

    with json_repo._repo_path.open("r") as f:
        invoices = json.load(f)
    assert invoices[0] == invoice1.json()


def test_create_invoice_appends_to_repo_file(json_repo, invoice1, invoice2):
    json_repo.create_invoice(invoice1)
    json_repo.create_invoice(invoice2)

    with json_repo._repo_path.open("r") as f:
        invoices = json.load(f)

    assert invoices == [invoice1.json(), invoice2.json()]


def test_read_invoice_returns_correct_invoice(json_repo, invoice1, invoice2):
    json_repo.create_invoice(invoice1)
    json_repo.create_invoice(invoice2)

    invoice = json_repo.read_invoice(reference=invoice2.reference)

    assert invoice == invoice2


def test_delete_invoice_deletes_correct_invoice(json_repo, invoice1, invoice2):
    json_repo.create_invoice(invoice1)
    json_repo.create_invoice(invoice2)

    json_repo.delete_invoice(invoice1.reference)

    assert invoice1 not in json_repo._invoices


def test_update_invoice_updates_correct_invoice(json_repo, invoice1):
    json_repo.create_invoice(invoice1)
    invoice1.pay()
    json_repo.update_invoice(invoice1)

    invoice = json_repo.read_invoice(invoice1.reference)

    assert invoice.is_paid


def test_list_all_returns_list_of_all_invoices(json_repo, invoice1, invoice2):
    json_repo.create_invoice(invoice1)
    json_repo.create_invoice(invoice2)

    invoices = json_repo.list_all()

    assert invoices == [invoice1, invoice2]
