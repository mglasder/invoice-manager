import json
from datetime import datetime
import pytest
from invoice_manager.core.invoice_lister import InvoiceLister
from invoice_manager.core.json_repository import InvoiceJsonRepository
from invoice_manager.models.invoice import Invoice
from invoice_manager.models.refundstatus import RefundStatus
from invoice_manager.models.options import LogicalOperator


@pytest.fixture
def invoices():
    with open("example_invoices.json") as f:
        invs = json.load(f)
    return [Invoice(**inv) for inv in invs]


@pytest.fixture
def mock_json_repo_file(tmp_path):
    repo_path = tmp_path / "invoices.json"
    return repo_path


@pytest.fixture
def json_repo(mock_json_repo_file):
    return InvoiceJsonRepository(mock_json_repo_file)


@pytest.fixture
def evaluator(json_repo):
    return InvoiceLister(repo=json_repo)


def test__filter_payment_status(evaluator, json_repo, invoices):
    for invoice in invoices:
        json_repo.create_invoice(invoice)

    invoices_unpaid = evaluator._filter_payment_status(is_paid=False)

    assert invoices_unpaid == invoices[:2]


def test__filter_refund_status(evaluator, json_repo, invoices):
    for invoice in invoices:
        json_repo.create_invoice(invoice)

    invoices_unpaid = evaluator._filter_refund_status(refund_status=RefundStatus.OPEN)

    assert invoices_unpaid == [invoices[0], invoices[2]]


def test__logical_combine_AND(evaluator, invoices):
    inv_paid = invoices[2:]
    inv_open = [invoices[0], invoices[2]]

    invs_out = evaluator._logical_combine(inv_paid, inv_open, LogicalOperator.AND)

    assert invs_out == [invoices[2]]


def test__logical_combine_OR(evaluator, invoices):
    inv_paid = invoices[2:]
    inv_open = [invoices[0], invoices[2]]

    invs_out = evaluator._logical_combine(inv_paid, inv_open, LogicalOperator.OR)

    assert invs_out == [invoices[0], invoices[2], invoices[3]]


def test_filter_invoices_payment_status(evaluator, json_repo, invoices):
    for invoice in invoices:
        json_repo.create_invoice(invoice)

    invoices_unpaid = evaluator.filter_invoices(
        is_paid=False, refund_status=None, operator=LogicalOperator.AND
    )

    assert invoices_unpaid == invoices[:2]


def test_filter_invoices_refund_status(evaluator, json_repo, invoices):
    for invoice in invoices:
        json_repo.create_invoice(invoice)

    invoices_paid = evaluator.filter_invoices(
        is_paid=True, refund_status=None, operator=LogicalOperator.AND
    )

    assert invoices_paid == invoices[2:]


def test_filter_payment_status_AND_refund_status(evaluator, json_repo, invoices):
    for invoice in invoices:
        json_repo.create_invoice(invoice)

    invs_out = evaluator.filter_invoices(
        is_paid=True, refund_status=RefundStatus.OPEN, operator=LogicalOperator.AND
    )

    assert invs_out == [invoices[2]]


def test_filter_payment_status_OR_refund_status(evaluator, json_repo, invoices):
    for invoice in invoices:
        json_repo.create_invoice(invoice)

    invs_out = evaluator.filter_invoices(
        is_paid=True, refund_status=RefundStatus.OPEN, operator=LogicalOperator.OR
    )

    assert invs_out == [invoices[0], invoices[2], invoices[3]]
