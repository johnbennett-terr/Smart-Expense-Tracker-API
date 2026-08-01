import os
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, HTTPException, Query

from src.models import Expense, ExpenseCreate
from src.storage import ExpenseStorage

app = FastAPI(title="Smart Expense Tracker")

_data_file_env = os.environ.get("EXPENSE_DATA_FILE")
storage = ExpenseStorage(data_file=Path(_data_file_env)) if _data_file_env else ExpenseStorage()


@app.get("/")
def root():
    return {"status": "ok"}


@app.post("/expenses", response_model=Expense, status_code=201)
def create_expense(expense: ExpenseCreate):
    return storage.add(expense)


# Declared before /expenses/{expense_id} so "total" isn't swallowed as an id.
@app.get("/expenses/total")
def get_total(category: Optional[str] = Query(default=None)):
    expenses = storage.list_all(category=category)
    total = sum(e.amount for e in expenses)
    return {"total": total, "category": category}


@app.get("/expenses", response_model=list[Expense])
def list_expenses(category: Optional[str] = Query(default=None)):
    return storage.list_all(category=category)


@app.get("/expenses/{expense_id}", response_model=Expense)
def get_expense(expense_id: int):
    expense = storage.get(expense_id)
    if expense is None:
        raise HTTPException(status_code=404, detail="Expense not found")
    return expense


@app.delete("/expenses/{expense_id}", status_code=204)
def delete_expense(expense_id: int):
    deleted = storage.delete(expense_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Expense not found")
