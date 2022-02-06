class InvoiceNonexistent(Exception):
    pass


class InvoiceNotFound(Exception):
    pass


class InvoiceAlreadyExists(Exception):
    pass


class RefundStatusCannotChange(Exception):
    pass
