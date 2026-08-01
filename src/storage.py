import json
import threading
from pathlib import Path

from src.models import Expense, ExpenseCreate

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_DATA_FILE = PROJECT_ROOT / "expenses.json"


class ExpenseStorage:
    """JSON-file-backed store for expenses, safe for concurrent access within one process."""

    def __init__(self, data_file: Path = DEFAULT_DATA_FILE):
        self.data_file = Path(data_file)
        self._lock = threading.Lock()
        if not self.data_file.exists():
            self._write_all([])

    def _read_all(self) -> list[dict]:
        """Load the full list of expense records from disk."""
        with self.data_file.open("r", encoding="utf-8") as f:
            return json.load(f)

    def _write_all(self, expenses: list[dict]) -> None:
        """Overwrite the data file with the full list of expense records."""
        with self.data_file.open("w", encoding="utf-8") as f:
            json.dump(expenses, f, indent=2)

    def add(self, expense: ExpenseCreate) -> Expense:
        """Assign the next id and persist a new expense. Read-modify-write is lock-protected."""
        with self._lock:
            expenses = self._read_all()
            next_id = max((e["id"] for e in expenses), default=0) + 1
            record = Expense(id=next_id, **expense.model_dump())
            expenses.append(record.model_dump(mode="json"))
            self._write_all(expenses)
            return record

    def list_all(self, category: str | None = None) -> list[Expense]:
        """Return all expenses, optionally filtered to one category (case-insensitive)."""
        with self._lock:
            expenses = self._read_all()
        if category is not None:
            expenses = [
                e for e in expenses if e["category"].lower() == category.lower()
            ]
        return [Expense(**e) for e in expenses]

    def get(self, expense_id: int) -> Expense | None:
        """Return the expense with the given id, or None if it doesn't exist."""
        with self._lock:
            expenses = self._read_all()
        for e in expenses:
            if e["id"] == expense_id:
                return Expense(**e)
        return None

    def delete(self, expense_id: int) -> bool:
        """Delete the expense with the given id. Returns True if removed, False if not found."""
        with self._lock:
            expenses = self._read_all()
            remaining = [e for e in expenses if e["id"] != expense_id]
            if len(remaining) == len(expenses):
                return False
            self._write_all(remaining)
            return True
