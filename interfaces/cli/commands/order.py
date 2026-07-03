import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer()
console = Console()


@app.command()
def create_order(
    customer_id: str = typer.Option(..., help="Customer ID"),
) -> None:
    """Create a new order."""
    console.print(f"Creating order for customer: {customer_id}")
    console.print("✓ Order created successfully")


@app.command()
def list_orders(
    customer_id: str = typer.Option(None, help="Filter by customer ID"),
    status: str = typer.Option(None, help="Filter by status"),
) -> None:
    """List orders."""
    table = Table(title="Orders")
    table.add_column("Order ID", style="cyan")
    table.add_column("Customer ID", style="magenta")
    table.add_column("Status", style="green")
    table.add_column("Total", justify="right")
    table.add_column("Date", style="yellow")

    # Sample data
    table.add_row("ORD-001", "CUST-001", "delivered", "$250.00", "2024-01-15")
    table.add_row("ORD-002", "CUST-002", "shipped", "$175.50", "2024-01-16")
    table.add_row("ORD-003", "CUST-001", "processing", "$500.00", "2024-01-17")

    console.print(table)


@app.command()
def get_order(
    order_id: str = typer.Argument(..., help="Order ID"),
) -> None:
    """Get order details."""
    console.print(f"Order Details: {order_id}")
    console.print("Customer: CUST-001")
    console.print("Status: processing")
    console.print("Total: $500.00")
