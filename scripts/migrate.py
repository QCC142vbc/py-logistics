#!/usr/bin/env python3
"""
Run database migrations using Alembic.
"""

import subprocess
import sys


def main():
    """Run Alembic migrations."""
    command = sys.argv[1] if len(sys.argv) > 1 else "upgrade"
    
    if command == "upgrade":
        subprocess.run(["alembic", "upgrade", "head"])
    elif command == "downgrade":
        subprocess.run(["alembic", "downgrade", "-1"])
    elif command == "revision":
        message = sys.argv[2] if len(sys.argv) > 2 else "auto migration"
        subprocess.run(["alembic", "revision", "--autogenerate", "-m", message])
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)


if __name__ == "__main__":
    main()
