import os
from pathlib import Path

from fastapi import FastAPI, HTTPException, Query

from src.models import Expense, ExpenseCreate
from src.storage import ExpenseStorage

app = FastAPI(title="Smart Expense Tracker")

_data_file_env = os.environ.get("EXPENSE_DATA_FILE")
storage = (
    ExpenseStorage(data_file=Path(_data_file_env))
    if _data_file_env
    else ExpenseStorage()
)


@app.get("/")
def root():
    """Health check. Returns 200 with a static status payload."""
    return {"status": "ok"}


@app.post("/expenses", response_model=Expense, status_code=201)
def create_expense(expense: ExpenseCreate):
    """Create a new expense. Returns the stored expense with its assigned id, 201 on success."""
    return storage.add(expense)


# Declared before /expenses/{expense_id} so "total" isn't swallowed as an id.
@app.get("/expenses/total")
def get_total(category: str | None = Query(default=None)):
    """Return the summed amount of all expenses, optionally filtered by category (case-insensitive)."""
    expenses = storage.list_all(category=category)
    total = sum(e.amount for e in expenses)
    return {"total": total, "category": category}


@app.get("/expenses", response_model=list[Expense])
def list_expenses(category: str | None = Query(default=None)):
    """List all expenses, optionally filtered by category (case-insensitive)."""
    return storage.list_all(category=category)


@app.get("/expenses/{expense_id}", response_model=Expense)
def get_expense(expense_id: int):
    """Fetch a single expense by id. Returns 404 if no expense with that id exists."""
    expense = storage.get(expense_id)
    if expense is None:
        raise HTTPException(status_code=404, detail="Expense not found")
    return expense


@app.delete("/expenses/{expense_id}", status_code=204)
def delete_expense(expense_id: int):
    """Delete a single expense by id. Returns 204 on success, 404 if no expense with that id exists."""
    deleted = storage.delete(expense_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Expense not found")
