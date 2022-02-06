import smtplib
from typing import List, Optional
import yagmail


class GmailService:
    def __init__(
        self, recipient: str, sender: str, subject: str, creds=str, debug=False
    ):
        self.debug = debug
        self.sender = sender
        self.recipient = recipient
        self.subject = subject
        if debug:
            self._server = "localhost"
            self._port = 1025
        else:
            self._creds = creds

    def send_mail(
        self,
        message: str,
        attach: Optional[List[str]] = None,
    ):
        if self.debug:
            self._send_mail_debug(message, self.recipient)
        else:
            self._send_mail(self.subject, message, self.recipient, attach)

    def _send_mail_debug(self, message: str, to: str):
        with smtplib.SMTP(self._server, self._port) as server:
            server.sendmail(self.sender, to, message)

    def _send_mail(
        self, subject: Optional[str], message: str, to: str, attach: Optional[List[str]]
    ):
        with yagmail.SMTP(self.sender, self._creds) as server:
            server.send(
                to=to,
                subject=subject,
                contents=message,
                attachments=attach,
            )
