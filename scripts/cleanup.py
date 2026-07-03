#!/usr/bin/env python3
"""
Cleanup script for the logistics system.
"""

import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from src.infrastructure.database.connection import DatabaseConnection, DatabaseConfig


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
        # Clean up old logs (older than 90 days)
        await session.execute(
            text("DELETE FROM audit_logs WHERE created_at < NOW() - INTERVAL '90 days'")
        )
        
        # Clean up old events (older than 180 days)
        await session.execute(
            text("DELETE FROM domain_events WHERE occurred_at < NOW() - INTERVAL '180 days'")
        )
        
        await session.commit()
        print("Cleanup completed successfully!")
    
    await db.disconnect()


if __name__ == "__main__":
    asyncio.run(main())
