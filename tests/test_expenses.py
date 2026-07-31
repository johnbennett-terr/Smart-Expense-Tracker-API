import pytest
from fastapi.testclient import TestClient

from src import main
from src.storage import ExpenseStorage

VALID_EXPENSE = {
    "title": "Coffee",
    "amount": 4.5,
    "category": "Food",
    "date": "2026-08-01",
}


@pytest.fixture
def client(tmp_path, monkeypatch):
    data_file = tmp_path / "expenses.json"
    monkeypatch.setattr(main, "storage", ExpenseStorage(data_file=data_file))
    return TestClient(main.app)


def test_create_expense_happy_path(client):
    response = client.post("/expenses", json=VALID_EXPENSE)
    assert response.status_code == 201
    body = response.json()
    assert body["id"] == 1
    assert body["title"] == "Coffee"
    assert body["amount"] == 4.5
    assert body["category"] == "Food"
    assert body["date"] == "2026-08-01"


def test_create_expense_blank_title_rejected(client):
    response = client.post("/expenses", json={**VALID_EXPENSE, "title": "   "})
    assert response.status_code == 422


def test_create_expense_blank_category_rejected(client):
    response = client.post("/expenses", json={**VALID_EXPENSE, "category": ""})
    assert response.status_code == 422


def test_create_expense_zero_amount_rejected(client):
    response = client.post("/expenses", json={**VALID_EXPENSE, "amount": 0})
    assert response.status_code == 422


def test_create_expense_negative_amount_rejected(client):
    response = client.post("/expenses", json={**VALID_EXPENSE, "amount": -5})
    assert response.status_code == 422


def test_create_expense_malformed_date_rejected(client):
    response = client.post("/expenses", json={**VALID_EXPENSE, "date": "not-a-date"})
    assert response.status_code == 422


def test_list_expenses_empty(client):
    response = client.get("/expenses")
    assert response.status_code == 200
    assert response.json() == []


def test_list_and_filter_by_category(client):
    client.post("/expenses", json=VALID_EXPENSE)
    client.post("/expenses", json={**VALID_EXPENSE, "title": "Bus", "category": "Transport"})

    response = client.get("/expenses")
    assert len(response.json()) == 2

    response = client.get("/expenses", params={"category": "Food"})
    body = response.json()
    assert len(body) == 1
    assert body[0]["category"] == "Food"


def test_filter_by_category_with_no_matches(client):
    client.post("/expenses", json=VALID_EXPENSE)

    response = client.get("/expenses", params={"category": "Nonexistent"})
    assert response.status_code == 200
    assert response.json() == []


def test_get_expense_by_id(client):
    created = client.post("/expenses", json=VALID_EXPENSE).json()

    response = client.get(f"/expenses/{created['id']}")
    assert response.status_code == 200
    assert response.json()["id"] == created["id"]


def test_get_expense_not_found(client):
    response = client.get("/expenses/9999")
    assert response.status_code == 404


def test_delete_expense(client):
    created = client.post("/expenses", json=VALID_EXPENSE).json()

    response = client.delete(f"/expenses/{created['id']}")
    assert response.status_code == 204

    response = client.get(f"/expenses/{created['id']}")
    assert response.status_code == 404


def test_delete_nonexistent_expense_returns_404(client):
    response = client.delete("/expenses/9999")
    assert response.status_code == 404


def test_total_overall(client):
    client.post("/expenses", json=VALID_EXPENSE)
    client.post("/expenses", json={**VALID_EXPENSE, "title": "Bus", "category": "Transport", "amount": 2.0})

    response = client.get("/expenses/total")
    assert response.status_code == 200
    assert response.json()["total"] == 6.5


def test_total_by_category(client):
    client.post("/expenses", json=VALID_EXPENSE)
    client.post("/expenses", json={**VALID_EXPENSE, "title": "Lunch", "amount": 10.0})
    client.post("/expenses", json={**VALID_EXPENSE, "title": "Bus", "category": "Transport", "amount": 2.0})

    response = client.get("/expenses/total", params={"category": "Food"})
    assert response.status_code == 200
    assert response.json()["total"] == 14.5


def test_total_by_category_with_no_matches(client):
    client.post("/expenses", json=VALID_EXPENSE)

    response = client.get("/expenses/total", params={"category": "Nonexistent"})
    assert response.status_code == 200
    assert response.json()["total"] == 0


def test_data_survives_storage_restart(tmp_path, monkeypatch):
    data_file = tmp_path / "expenses.json"
    monkeypatch.setattr(main, "storage", ExpenseStorage(data_file=data_file))
    client1 = TestClient(main.app)
    created = client1.post("/expenses", json=VALID_EXPENSE).json()

    # Simulate a server restart: a fresh storage instance backed by the same file.
    monkeypatch.setattr(main, "storage", ExpenseStorage(data_file=data_file))
    client2 = TestClient(main.app)
    response = client2.get(f"/expenses/{created['id']}")
    assert response.status_code == 200
    assert response.json()["title"] == "Coffee"
