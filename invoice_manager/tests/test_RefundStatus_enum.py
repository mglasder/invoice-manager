from invoice_manager.models.refundstatus import RefundStatus


def test_RefundStatus_enum():

    assert RefundStatus.OPEN.value == "open"
    assert RefundStatus.REQUESTED.value == "requested"
    assert RefundStatus.CONFIRMED.value == "confirmed"
    assert RefundStatus.DECLINED.value == "declined"
    assert RefundStatus.COMPLETED.value == "completed"
