import pytest
from fastapi.testclient import TestClient

from src.interfaces.api.main import app


@pytest.fixture
def client():
    """Create a test client for the API."""
    return TestClient(app)


class TestInventoryAPI:
    def test_list_items(self, client):
        response = client.get("/api/v1/inventory/items")
        assert response.status_code == 200
        data = response.json()
        assert "items" in data
        assert "total" in data

    def test_create_item(self, client):
        response = client.post(
            "/api/v1/inventory/items",
            json={
                "sku": "TEST-001",
                "name": "Test Item",
                "quantity": 100,
                "unit_cost": 25.00,
                "location": "WH-A-01",
                "category": "widgets",
                "reorder_point": 20,
                "lead_time_days": 7,
            },
        )
        assert response.status_code == 201
        data = response.json()
        assert "id" in data


class TestOrdersAPI:
    def test_list_orders(self, client):
        response = client.get("/api/v1/orders/")
        assert response.status_code == 200
        data = response.json()
        assert "orders" in data

    def test_create_order(self, client):
        response = client.post(
            "/api/v1/orders/",
            json={
                "customer_id": "cust-001",
                "items": [{"item_id": "item-001", "sku": "ITEM-001", "quantity": 10, "unit_price": 25.00}],
                "shipping_address": {"street": "123 Main St", "city": "Test City", "state": "TS", "postal_code": "12345", "country": "USA"},
                "billing_address": {"street": "123 Main St", "city": "Test City", "state": "TS", "postal_code": "12345", "country": "USA"},
            },
        )
        assert response.status_code == 201
