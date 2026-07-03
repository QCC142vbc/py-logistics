#!/usr/bin/env python3
"""
Seed the database with initial data.
"""

import asyncio
from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.database.connection import DatabaseConnection, DatabaseConfig
from src.infrastructure.database.seed_data import seed_all


async def main():
    config = DatabaseConfig(
        host="localhost",
        port=5432,
        database="logistics_db",
        username="logistics",
        password="password",
    )
    
    db = DatabaseConnection(config)
    await db.connect()
    
    async with db.get_session() as session:
        await seed_all(session)
        print("Database seeded successfully!")
    
    await db.disconnect()


if __name__ == "__main__":
    asyncio.run(main())
