import pytest
from fastapi.testclient import TestClient
from src.api.main import app


@pytest.fixture
def client():
    return TestClient(app)


def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_root(client):
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert data["docs"] == "/docs"


def test_create_supplier(client):
    response = client.post(
        "/api/v1/suppliers",
        json={
            "name": "Test Supplier",
            "email": "test@example.com",
            "phone": "555-0100",
            "rating": 4.5,
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Supplier"
    assert "id" in data


def test_create_item(client):
    response = client.post(
        "/api/v1/items",
        json={
            "sku": "TEST-001",
            "name": "Test Item",
            "quantity": 100,
            "unit_cost": 25.00,
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["sku"] == "TEST-001"
    assert "id" in data


def test_list_items(client):
    # First create an item
    client.post(
        "/api/v1/items",
        json={
            "sku": "TEST-001",
            "name": "Test Item",
            "quantity": 100,
            "unit_cost": 25.00,
        },
    )
    
    # Then list items
    response = client.get("/api/v1/items")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1
