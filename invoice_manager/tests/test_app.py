import pytest
from typer.testing import CliRunner
from invoice_manager.app import app


@pytest.fixture
def runner():
    return CliRunner()


def test_app_startup(runner):
    result = runner.invoke(app)


def test_invoices_list_command(runner):
    result = runner.invoke(app, ["list"])


def test_add_command_adds_invoice_to_repo(runner):
    result = runner.invoke(app, ["add", "2020-01-01", "ABClabs", "001", 123.45])
    # TODO: Find out what's wrong here
    # assert result.exit_code == 0
    # assert "Invoice created with reference: '001_ABClabs'" in result.stdout
    # TODO: Find out how to access repo properly
    # assert len(invoice_processor.repo.invoices) == 1
