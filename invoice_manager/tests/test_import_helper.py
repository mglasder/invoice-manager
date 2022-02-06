from datetime import datetime
from pathlib import Path

import pytest
from invoice_manager.core.importer import FileImporter
from invoice_manager.models.invoice import Invoice


@pytest.fixture
def helper():
    return FileImporter()


@pytest.fixture
def dirpath1():
    return Path("test_invoice_folder/subdir")


@pytest.fixture
def mock_repo():
    repo = []
    return repo


@pytest.fixture
def mock_add(mock_repo):
    def add(creation_date: str, issuer: str, nr: str, amount: float):
        date = datetime.strptime(creation_date, "%Y-%m-%d")
        mock_repo.append(
            Invoice(
                creation_date=date,
                issuer=issuer,
                nr=nr,
                amount=amount,
            )
        )

    return add


@pytest.fixture
def dirpath2():
    return Path("test_invoice_folder/subdir2")


def test_importing_files_and_return_as_list_of_dict(
    helper, dirpath1, mock_add, mock_repo
):

    helper.import_raw_from(dirpath1, on_finish_import=mock_add)

    expected_invoice = Invoice(
        **{
            "creation_date": "230410",
            "issuer": "ABC",
            "nr": "1234",
            "amount": 50.50,
        }
    )

    assert mock_repo[0].reference == expected_invoice.reference


def test_importing_multiple_files(helper, dirpath2, mock_add, mock_repo):
    helper.import_raw_from(dirpath2, on_finish_import=mock_add)
    assert len(mock_repo) == 2
