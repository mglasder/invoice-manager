import json
import os
from pathlib import Path

import yaml

from invoice_manager.core.importer import FileImporter
from invoice_manager.core.invoice_lister import InvoiceLister
from invoice_manager.core.invoice_processor import InvoiceCreator, PaymentProcessor
from invoice_manager.core.json_repository import InvoiceJsonRepository
from invoice_manager.mail.gmail import GmailService
from invoice_manager.models.config import RepoConfig, AppConfig
from invoice_manager.core.refund_processor import RefundProcessor
from invoice_manager.core.stats_calculator import StatsCalculator
from invoice_manager.core.requester import RequestManager


class AppManager:
    def __init__(self, app_dir: Path):
        self._app_dir = app_dir
        self._setup()
        self.inv_directory = self._app_config.invoice_directory
        self.refund_processor = RefundProcessor(repo=self._repo)
        self.invoice_creator = InvoiceCreator(repo=self._repo)
        self.payment_processor = PaymentProcessor(repo=self._repo)
        self.invoice_lister = InvoiceLister(repo=self._repo)
        self.stats_calculator = StatsCalculator(repo=self._repo)
        self.importer = FileImporter()
        self.mail_service = GmailService(
            recipient=self._app_config.recipient,
            subject=self._app_config.mail_subject,
            sender=self._app_config.sender,
            creds=self._app_config.gmail_credentials,
        )
        self.request_manager = RequestManager(
            self.mail_service,
            self.refund_processor,
            self.inv_directory,
            self._app_config.signature,
        )

    def _setup(self):
        self._app_config = self._load_app_config(path=(self._app_dir / "config.yaml"))

        self._default_repopath = (
            self._app_config.repo_directory / "default-invoices.json"
        )
        self._repo = self._create_repo(self._default_repopath)

    @staticmethod
    def _load_app_config(path: Path):
        config = AppConfig.parse_file(path, proto="yaml")
        return config

    @staticmethod
    def _create_repo(repo_path: Path) -> InvoiceJsonRepository:
        return InvoiceJsonRepository(repo_path=repo_path)
