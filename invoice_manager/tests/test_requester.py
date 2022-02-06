import json
from datetime import datetime
from pathlib import Path
import pytest

from invoice_manager.core.refund_processor import RefundProcessor
from invoice_manager.core.repository import InvoiceMemoryRepository
from invoice_manager.mail.gmail import GmailService
from invoice_manager.models.invoice import Invoice
from invoice_manager.core.requester import RequestManager


@pytest.fixture
def invoices():
    with open("example_invoices.json") as f:
        invs = json.load(f)
    return [Invoice(**inv) for inv in invs]


@pytest.fixture
def invoice1():
    invoice = Invoice(
        creation_date=datetime.strptime("2023-04-10", "%Y-%m-%d"),
        issuer="ABC",
        nr="1234",
        amount=50.50,
    )
    return invoice


@pytest.fixture
def directory():
    directory = Path("test_invoice_folder")
    return directory


@pytest.fixture
def gmail():
    return GmailService(
        recipient="recipient@test.com",
        sender="sender@test.com",
        subject="TestMail",
        creds="xxx",
        debug=True,
    )


@pytest.fixture
def repo():
    return InvoiceMemoryRepository()


@pytest.fixture
def refund_processor(repo):
    return RefundProcessor(repo)


def test_write_email(gmail, invoices, refund_processor, directory):

    requester = RequestManager(
        mail_service=gmail,
        refund_processor=refund_processor,
        directory=directory,
        signature="Joe Doe",
    )

    mail = requester._compose_email()
    print(mail)


def test_collect_attachments(invoice1, gmail, repo, refund_processor, directory):
    requester = RequestManager(
        mail_service=gmail,
        refund_processor=refund_processor,
        directory=directory,
        signature="Joe Doe",
    )

    repo.create_invoice(invoice1)

    requester.request_refunds(["290122f0"], mail=False)

    requester._collect_attachements()
    invs = [
        "subdir/230410_ABC_1234_50.50.pdf",
    ]
    expected_paths = [Path(directory, fname) for fname in invs]

    found_paths = [Path(item) for item in requester._attachments]

    assert found_paths == expected_paths
