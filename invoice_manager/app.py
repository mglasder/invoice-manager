import os
from pathlib import Path
from typing import List
import typer
from invoice_manager import refund
from invoice_manager.manager import AppManager
from invoice_manager.models.options import (
    PaymentFilterOptions,
    RefundFilterOptions,
    LogicalOperator,
    OptionsMapping,
)
from invoice_manager.models.exceptions import InvoiceNonexistent, InvoiceAlreadyExists
from invoice_manager.ui.invoice_table import InvoiceTable
from invoice_manager.ui.stats_table import StatsTable


app = typer.Typer()
app.add_typer(refund.app, name="refund")

app_dir = Path(os.path.dirname(os.path.realpath(__file__))).parent
manager = AppManager(app_dir=app_dir)


@app.command(name="new-repo")
def new_repo(name: str):
    """Create new invoice manager."""
    # TODO: implement
    pass


@app.command(name="switch-repo")
def switch_repo():
    # TODO: Implement use -> changes to repos
    """Choose repository by name."""
    pass


@app.command(name="import")
def add_from_dir(folder: str):
    """Import invoices from folder and add to repo."""
    manager.importer.import_raw_from(folder, on_finish_import=add)


@app.command()
def add(creation_date: str, issuer: str, nr: str, amount: float):
    """Add new invoice(s)."""
    try:
        ref = manager.invoice_creator.add_invoice(creation_date, issuer, nr, amount)
        typer.echo(f"Invoice created with reference: '{ref}'")
    except InvoiceAlreadyExists as e:
        typer.echo(f"Invoice {e} already exists.")


@app.command()
def delete(references: List[str]):
    """Delete invoice(s). This cannot be undone!"""
    typer.confirm("Do you want to delete invoice(s)?", abort=True)
    for ref in references:
        try:
            manager.invoice_creator.delete_invoice(ref)
            typer.echo(f"'{ref}': Invoice deleted.")
        except InvoiceNonexistent:
            typer.echo(f"'{ref}': Invoice does not exist.")


@app.command()
def pay(references: List[str]):
    """Pay invoice(s)."""
    for ref in references:
        try:
            manager.payment_processor.pay_invoice(ref)
            typer.echo(f"'{ref}': Invoice has been paid.")
        except InvoiceNonexistent:
            typer.echo(f"'{ref}': Invoice does not exist.")


@app.command(name="list")
def list_invoices(
    ps: PaymentFilterOptions = typer.Option(
        PaymentFilterOptions.any.value,
        help="PAYMENT STATUS: choose option to filter what is listed",
    ),
    rs: RefundFilterOptions = typer.Option(
        RefundFilterOptions.any.value,
        help="REFUND STATUS: choose option to filter what is listed",
    ),
    operator: LogicalOperator = typer.Option(
        LogicalOperator.AND.value, help="Choose operator two combine both filters"
    ),
):
    """List invoices with payment and refund status (according to filter)."""

    is_paid = OptionsMapping.payment[ps]
    refund_status = OptionsMapping.refund[rs]

    invoices = manager.invoice_lister.filter_invoices(
        is_paid=is_paid, refund_status=refund_status, operator=operator
    )

    table = InvoiceTable()
    typer.echo(table.create(invoices))


@app.command(name="stats")
def show_stats():
    """Show stats for invoices."""

    payment_stats = manager.stats_calculator.payment_stats
    refund_stats = manager.stats_calculator.refund_stats

    stats = StatsTable()
    ps_table, rs_table = stats.create(
        payment_stats=payment_stats, refund_stats=refund_stats
    )
    typer.echo(ps_table)
    typer.echo(rs_table)


if __name__ == "__main__":
    app()
