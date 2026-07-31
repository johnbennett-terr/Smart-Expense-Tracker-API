import json
import threading
from pathlib import Path
from typing import Optional

from src.models import Expense, ExpenseCreate

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_DATA_FILE = PROJECT_ROOT / "expenses.json"


class ExpenseStorage:
    def __init__(self, data_file: Path = DEFAULT_DATA_FILE):
        self.data_file = Path(data_file)
        self._lock = threading.Lock()
        if not self.data_file.exists():
            self._write_all([])

    def _read_all(self) -> list[dict]:
        with self.data_file.open("r", encoding="utf-8") as f:
            return json.load(f)

    def _write_all(self, expenses: list[dict]) -> None:
        with self.data_file.open("w", encoding="utf-8") as f:
            json.dump(expenses, f, indent=2)

    def add(self, expense: ExpenseCreate) -> Expense:
        with self._lock:
            expenses = self._read_all()
            next_id = max((e["id"] for e in expenses), default=0) + 1
            record = Expense(id=next_id, **expense.model_dump())
            expenses.append(record.model_dump(mode="json"))
            self._write_all(expenses)
            return record

    def list_all(self, category: Optional[str] = None) -> list[Expense]:
        with self._lock:
            expenses = self._read_all()
        if category is not None:
            expenses = [e for e in expenses if e["category"] == category]
        return [Expense(**e) for e in expenses]

    def get(self, expense_id: int) -> Optional[Expense]:
        with self._lock:
            expenses = self._read_all()
        for e in expenses:
            if e["id"] == expense_id:
                return Expense(**e)
        return None

    def delete(self, expense_id: int) -> bool:
        with self._lock:
            expenses = self._read_all()
            remaining = [e for e in expenses if e["id"] != expense_id]
            if len(remaining) == len(expenses):
                return False
            self._write_all(remaining)
            return True

    def search(self, category: Optional[str] = None) -> list[Expense]:
        return self.list_all(category=category)
