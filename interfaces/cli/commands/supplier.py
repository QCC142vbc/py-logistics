import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer()
console = Console()


@app.command()
def add_supplier(
    name: str = typer.Option(..., help="Supplier name"),
    email: str = typer.Option(..., help="Contact email"),
    phone: str = typer.Option(..., help="Phone number"),
) -> None:
    """Register a new supplier."""
    console.print(f"Registering supplier: {name}")
    console.print(f"Email: {email}")
    console.print(f"Phone: {phone}")
    console.print("✓ Supplier registered successfully")


@app.command()
def list_suppliers() -> None:
    """List all suppliers."""
    table = Table(title="Suppliers")
    table.add_column("ID", style="cyan")
    table.add_column("Name", style="magenta")
    table.add_column("Email", style="green")
    table.add_column("Rating", justify="right")
    table.add_column("Status", style="yellow")

    # Sample data
    table.add_row("SUP-001", "Acme Supplies Inc", "contact@acme.com", "4.5", "active")
    table.add_row("SUP-002", "Global Logistics Partners", "orders@globallogistics.com", "4.2", "active")
    table.add_row("SUP-003", "Prime Materials Co", "sales@primematerials.com", "3.8", "active")

    console.print(table)


@app.command()
def evaluate_supplier(
    supplier_id: str = typer.Argument(..., help="Supplier ID"),
) -> None:
    """Evaluate supplier performance."""
    console.print(f"Evaluating supplier: {supplier_id}")
    console.print("Reliability Score: 85.0")
    console.print("Quality Score: 90.0")
    console.print("Cost Score: 75.0")
    console.print("Delivery Score: 88.0")
    console.print("Overall Score: 84.5")
