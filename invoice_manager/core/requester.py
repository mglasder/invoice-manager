import glob
from pathlib import Path
from typing import List
import typer
from invoice_manager.core.refund_processor import RefundProcessor
from invoice_manager.mail.gmail import GmailService
from invoice_manager.models.exceptions import InvoiceNotFound, RefundStatusCannotChange


class RequestManager:
    def __init__(
        self,
        mail_service: GmailService,
        refund_processor: RefundProcessor,
        directory: Path,
        signature: str,
    ):
        self._refund_processor = refund_processor
        self._mail_service = mail_service
        self._signature = signature
        self._attachments = []
        self._dir = directory
        self._requestable_invoices = []

    def request_refunds(self, references: List[str], mail=False):
        for ref in references:
            try:
                invoice = self._refund_processor.request(ref)
                self._requestable_invoices.append(invoice)
            except InvoiceNotFound:
                typer.echo(f"'{ref}': Invoice does not exist.")
            except RefundStatusCannotChange as e:
                typer.echo(f"'{ref}': {e}")

        if mail:
            self._send_mail()

    def _send_mail(self):
        self._collect_attachements()
        body = self._compose_email()
        typer.echo(body)
        typer.confirm("Do you want to send above email?", abort=True)
        # TODO: reset requests to open if abort

        # TODO: move to, subject to config file
        self._mail_service.send_mail(
            message=body,
            attach=self._attachments,
        )

    def _compose_email(self):
        txt = ""
        for inv in self._requestable_invoices:
            txt += f"{inv.shortdate} - {inv.issuer} - {inv.nr}: {inv.amount:.2f} CHF\n"

        body = f"""
        Dear Sir or Madam,
        
        please refund the following invoices
        
        {txt}
        
        Thank you.
        Sincerely,
        
        {self._signature}
        """
        return body

    def _collect_attachements(self):
        files = []
        for inv in self._requestable_invoices:
            files.append(glob.glob(f"{self._dir}/**/{inv.filename}", recursive=True))
        self._attachments = [item for sublist in files for item in sublist]
