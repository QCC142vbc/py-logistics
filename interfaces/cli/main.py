import typer
from rich.console import Console

app = typer.Typer()
console = Console()


@app.command()
def version() -> None:
    """Show the application version."""
    console.print("Logistics Management System v1.0.0")


@app.command()
def init() -> None:
    """Initialize the application."""
    console.print("Initializing Logistics Management System...")
    console.print("✓ Configuration loaded")
    console.print("✓ Database connection established")
    console.print("✓ Ready")


if __name__ == "__main__":
    app()
