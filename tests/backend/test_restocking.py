"""
Tests for restocking API endpoints (recommendations + submitted orders).
"""
import json
from pathlib import Path

import pytest

import main


RESTOCKING_FILE = Path(main.DATA_DIR) / "restocking_orders.json"


@pytest.fixture
def restore_restocking_orders():
    """Snapshot the restocking orders file + in-memory list, restore after.

    The POST endpoint persists to disk and mutates the shared in-memory list,
    so tests that submit orders must leave both untouched for other tests/runs.
    """
    original_file = RESTOCKING_FILE.read_text()
    original_list = list(main.restocking_orders)
    try:
        yield
    finally:
        main.restocking_orders.clear()
        main.restocking_orders.extend(original_list)
        RESTOCKING_FILE.write_text(original_file)


class TestRestockingRecommendations:
    """Test suite for GET /api/restocking/recommendations."""

    def test_get_recommendations(self, client):
        """Recommendations return only positive demand-gap items with pricing."""
        response = client.get("/api/restocking/recommendations")
        assert response.status_code == 200

        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0

        for rec in data:
            assert "item_sku" in rec
            assert "item_name" in rec
            assert "trend" in rec
            # Only items where forecast exceeds current demand are recommended
            assert rec["forecasted_demand"] > rec["current_demand"]
            # Recommended quantity == the demand gap
            assert rec["recommended_quantity"] == rec["forecasted_demand"] - rec["current_demand"]
            assert rec["recommended_quantity"] > 0
            # Pricing is consistent
            assert isinstance(rec["unit_cost"], (int, float))
            assert rec["unit_cost"] > 0
            assert abs(rec["line_cost"] - rec["recommended_quantity"] * rec["unit_cost"]) < 0.01

    def test_recommendations_exclude_non_growing_demand(self, client):
        """Items with decreasing/flat demand (forecast <= current) are excluded."""
        response = client.get("/api/restocking/recommendations")
        skus = {rec["item_sku"] for rec in response.json()}
        # MTR-304 has forecasted_demand (35) < current_demand (50) in the mock data
        assert "MTR-304" not in skus

    def test_recommendations_sorted_by_priority(self, client):
        """Increasing-trend items rank ahead of non-increasing ones."""
        data = client.get("/api/restocking/recommendations").json()
        increasing_flags = [rec["trend"] == "increasing" for rec in data]
        # Once we hit a non-increasing item, no increasing item may follow
        assert increasing_flags == sorted(increasing_flags, reverse=True)


class TestRestockingOrders:
    """Test suite for GET/POST /api/restocking-orders."""

    def test_get_restocking_orders_returns_list(self, client):
        """The orders endpoint returns a list."""
        response = client.get("/api/restocking-orders")
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    def test_create_restocking_order(self, client, restore_restocking_orders):
        """Submitting an order computes totals, lead time, and persists it."""
        payload = {
            "items": [
                {"item_sku": "WDG-001", "item_name": "Industrial Widget Type A",
                 "quantity": 150, "unit_cost": 50.0},
                {"item_sku": "GSK-203", "item_name": "High-Temperature Gasket",
                 "quantity": 100, "unit_cost": 50.0},
            ]
        }
        response = client.post("/api/restocking-orders", json=payload)
        assert response.status_code == 200

        order = response.json()
        assert order["status"] == "Submitted"
        # Order number embeds the submission year (e.g. RSO-2026-0001)
        assert order["order_number"].startswith(f"RSO-{order['submitted_date'][:4]}-")
        assert order["lead_time_days"] == 14
        assert order["total_quantity"] == 250
        assert abs(order["total_cost"] - 12500.0) < 0.01
        # Expected delivery is in the future relative to the submitted date
        assert order["expected_delivery"] > order["submitted_date"]

        # The new order is retrievable and persisted to disk
        listed = client.get("/api/restocking-orders").json()
        assert any(o["order_number"] == order["order_number"] for o in listed)
        on_disk = json.loads(RESTOCKING_FILE.read_text())
        assert any(o["order_number"] == order["order_number"] for o in on_disk)

    def test_create_restocking_order_rejects_empty_items(self, client, restore_restocking_orders):
        """An order with no items is rejected with 400."""
        response = client.post("/api/restocking-orders", json={"items": []})
        assert response.status_code == 400
        assert "detail" in response.json()

    def test_create_restocking_order_drops_zero_quantity_items(self, client, restore_restocking_orders):
        """Zero-quantity lines are filtered out of the submitted order."""
        payload = {
            "items": [
                {"item_sku": "WDG-001", "item_name": "Industrial Widget Type A",
                 "quantity": 10, "unit_cost": 50.0},
                {"item_sku": "GSK-203", "item_name": "High-Temperature Gasket",
                 "quantity": 0, "unit_cost": 50.0},
            ]
        }
        response = client.post("/api/restocking-orders", json=payload)
        assert response.status_code == 200

        order = response.json()
        assert len(order["items"]) == 1
        assert order["items"][0]["item_sku"] == "WDG-001"
        assert order["total_quantity"] == 10

    def test_create_restocking_order_rejects_all_zero_quantity(self, client, restore_restocking_orders):
        """An order where every line is zero-quantity is rejected with 400."""
        payload = {
            "items": [
                {"item_sku": "WDG-001", "item_name": "Industrial Widget Type A",
                 "quantity": 0, "unit_cost": 50.0},
            ]
        }
        response = client.post("/api/restocking-orders", json=payload)
        assert response.status_code == 400
