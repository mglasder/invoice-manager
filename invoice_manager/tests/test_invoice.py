from datetime import datetime

import pytest

from invoice_manager.models.invoice import Invoice
from invoice_manager.models.refundstatus import RefundStatus


@pytest.fixture
def invoice():
    invoice = Invoice(
        creation_date=datetime.strptime("2022-01-01", "%Y-%m-%d"),
        issuer="TestLab",
        nr="6001ABC",
        amount=302.10,
    )
    return invoice


def test_invoice_refund_status_life_cycle(invoice):

    assert invoice.refund_status == RefundStatus.OPEN

    invoice.request_refund()
    assert invoice.refund_status == RefundStatus.REQUESTED

    invoice.recieve_request_confirmation()
    assert invoice.refund_status == RefundStatus.CONFIRMED

    invoice.recieve_request_decline()
    assert invoice.refund_status == RefundStatus.DECLINED

    invoice.recieve_refund()
    assert invoice.refund_status == RefundStatus.COMPLETED


def test_invoice_pay_method(invoice):

    assert invoice.is_paid is False
    invoice.pay()
    assert invoice.is_paid


def test_filename_is_correct(invoice):

    assert invoice.filename == "220101_TestLab_6001ABC_302.10.pdf"
