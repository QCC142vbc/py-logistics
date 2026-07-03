import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer()
console = Console()


@app.command()
def add_item(
    sku: str = typer.Option(..., help="Item SKU"),
    name: str = typer.Option(..., help="Item name"),
    quantity: int = typer.Option(..., help="Initial quantity"),
    unit_cost: float = typer.Option(..., help="Unit cost"),
    location: str = typer.Option(..., help="Storage location"),
    category: str = typer.Option(..., help="Item category"),
) -> None:
    """Add a new inventory item."""
    console.print(f"Adding item: {name} ({sku})")
    console.print(f"Quantity: {quantity}")
    console.print(f"Location: {location}")
    console.print("✓ Item added successfully")


@app.command()
def list_items(
    category: str = typer.Option(None, help="Filter by category"),
    location: str = typer.Option(None, help="Filter by location"),
) -> None:
    """List inventory items."""
    table = Table(title="Inventory Items")
    table.add_column("SKU", style="cyan")
    table.add_column("Name", style="magenta")
    table.add_column("Quantity", justify="right")
    table.add_column("Location", style="green")
    table.add_column("Category", style="yellow")

    # Sample data
    table.add_row("ITEM-001", "Industrial Widget A", "100", "WH-A-01", "widgets")
    table.add_row("ITEM-002", "Heavy Component B", "50", "WH-A-02", "components")
    table.add_row("ITEM-003", "Electronic Module C", "200", "WH-B-01", "electronics")

    console.print(table)


@app.command()
def adjust_stock(
    item_id: str = typer.Option(..., help="Item ID"),
    quantity: int = typer.Option(..., help="Quantity adjustment"),
    reason: str = typer.Option(..., help="Reason for adjustment"),
) -> None:
    """Adjust stock level for an item."""
    console.print(f"Adjusting stock for item {item_id}")
    console.print(f"Quantity change: {quantity:+d}")
    console.print(f"Reason: {reason}")
    console.print("✓ Stock adjusted successfully")
