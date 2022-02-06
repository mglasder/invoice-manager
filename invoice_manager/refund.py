import os
from pathlib import Path
from typing import List
import typer
from invoice_manager.manager import AppManager

app = typer.Typer()

app_dir = Path(os.path.dirname(os.path.realpath(__file__))).parent
manager = AppManager(app_dir=app_dir)


@app.command()
def request(
    references: List[str],
    mail: bool = typer.Option(
        False, help="Decide, whether to send refund request email."
    ),
):
    """Request refund(s) for invoice(s)."""
    manager.request_manager.request_refunds(references, mail=mail)


@app.command()
def confirmed(references: List[str]):
    """Mark refund request(s) as confirmed."""
    for ref in references:
        manager.refund_processor.confirm(ref)
        typer.echo(f"'{ref}': refund confirmed by insurance.")


@app.command()
def declined(references: List[str]):
    """Mark invoice(s)' refund status as declined."""
    for ref in references:
        manager.refund_processor.decline(ref)
        typer.echo(f"'{ref}': refund declined by insurance.")


@app.command()
def completed(references: List[str]):
    """Mark invoice(s) as completed."""
    for ref in references:
        manager.refund_processor.complete(ref)
        typer.echo(f"'{ref}': refund completed and money recieved.")


@app.command(name="rollback")
def rollback_to_open(references: List[str]):
    """Rollback refund status to 'open'."""
    typer.confirm("Do you want to rollback refund status?", abort=True)
    for ref in references:
        manager.refund_processor.rollback(ref)
        typer.echo(f"'{ref}': refund status rolled back to open.")
