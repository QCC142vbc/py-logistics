#!/usr/bin/env python3
"""
Generate reports for the logistics system.
"""

import asyncio
from datetime import datetime, timedelta

from src.analytics.reporting.report_generator import ReportGenerator, ReportFilter


async def main():
    generator = ReportGenerator()
    
    # Generate inventory report
    filter = ReportFilter(
        date_from=datetime.utcnow() - timedelta(days=30),
        date_to=datetime.utcnow(),
    )
    
    report = generator.generate_inventory_report(filter)
    print(f"Generated inventory report: {report.id}")
    print(f"Total items: {report.data['total_items']}")
    print(f"Total value: ${report.data['total_value']}")
    
    # Generate dashboard metrics
    metrics = generator.generate_dashboard_metrics(filter)
    print(f"\nDashboard Metrics:")
    print(f"Pending orders: {metrics.pending_orders}")
    print(f"In-transit shipments: {metrics.in_transit_shipments}")
    print(f"Low stock items: {metrics.low_stock_items}")
    print(f"System health: {metrics.system_health}")


if __name__ == "__main__":
    asyncio.run(main())
