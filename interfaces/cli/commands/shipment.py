import typer
from rich.console import Console

app = typer.Typer()
console = Console()


@app.command()
def track_shipment(
    tracking_number: str = typer.Argument(..., help="Tracking number"),
) -> None:
    """Track a shipment."""
    console.print(f"Tracking shipment: {tracking_number}")
    console.print("Status: In Transit")
    console.print("Current Location: Chicago, IL")
    console.print("Estimated Delivery: 2024-01-20")


@app.command()
def create_shipment(
    order_id: str = typer.Option(..., help="Order ID"),
) -> None:
    """Create a new shipment."""
    console.print(f"Creating shipment for order: {order_id}")
    console.print("✓ Shipment created successfully")
    console.print("Tracking Number: TRK-123456")
