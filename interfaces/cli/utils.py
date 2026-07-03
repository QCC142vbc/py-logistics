from typing import List, Dict
from rich.console import Console
from rich.table import Table


def print_table(data: List[Dict], columns: List[str]) -> None:
    """Print data as a formatted table."""
    console = Console()
    table = Table()
    
    for column in columns:
        table.add_column(column)
    
    for row in data:
        table.add_row(*[str(row.get(col, "")) for col in columns])
    
    console.print(table)


def confirm_action(message: str) -> bool:
    """Prompt user for confirmation."""
    console = Console()
    response = console.input(f"{message} [y/N]: ")
    return response.lower() in ["y", "yes"]
