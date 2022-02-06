# Invoice Manager

This is a CLI app to manage and process invoices. You can import invoices from pdf files and manage their status via the CLI interface.

To request refunds, the app uses the Gmail API to send out emails. The invoice files the refunds are requested for are attached to the email.

### Technologies

The app relies on the following main technologies:

- Pydantic for data modelling
- Typer for CLI
- Pytest for testing
- Gmail API for sending emails


### Simplified Class Structure

```mermaid
classDiagram

class InvoiceCLI

class RefundCLI

class InvoiceRepository {
    <<abstract>>
    +create_invoice()*
    +read_invoice()*
    +update_invoice()*
    +delete_invoice()*
    +list_all()*
}

class InvoiceJsonRepository

class InvoiceMemoryRepository

class InvoiceProcessor {
    -InvoiceRepository repo
    +add_invoice()
    +delete_invoice()
    +pay_invoice()
    +unpay_invoice()
}
class PaymentProcessor {
    -InvoiceRepository repo
}
class RefundProcessor {
    -InvoiceRepository repo
    +request()
    +confirm()
    +decline()
    +complete()
    +rollback()
}

class StatsCalculator {
    -InvoiceRepository repo
    -List<Invoice> invoices
    +List<float> payment_stats
    +List<float> refund_stats
    -calc_total()
    -calc_payment_status()
    -calc_refund_status()
}

class InvoiceLister {
    -InvoiceRepository repo
    -List<Invoice> invoices
    +filter_invoices()
    -filter_payment_status()
    -filter_refund_status()
    -logical_combine()
}

InvoiceCLI *.. RefundCLI

InvoiceCLI *.. InvoiceProcessor
InvoiceCLI *.. InvoiceLister
InvoiceCLI *.. PaymentProcessor
InvoiceCLI *.. StatsCalculator

RefundCLI *.. RefundProcessor

InvoiceRepository <|.. InvoiceJsonRepository : implements
InvoiceRepository <|.. InvoiceMemoryRepository : implements
  
InvoiceProcessor *.. InvoiceRepository 
PaymentProcessor *.. InvoiceRepository
RefundProcessor *.. InvoiceRepository
StatsCalculator *.. InvoiceRepository
InvoiceLister *.. InvoiceRepository
    

```

### Installation

To install the app, clone the repository and run the following command:

```bash

# Create environment using the exported environment file
conda env create -f conda.yml

# Activate environment
conda activate invoices39

# Install python dependencies
poetry install

# Start the CLI and have a look at the documentation
invoice --help

```
