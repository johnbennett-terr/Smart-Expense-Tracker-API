from datetime import date as date_type

from pydantic import BaseModel, Field, field_validator


class ExpenseCreate(BaseModel):
    """Client-supplied fields for a new expense, before an id is assigned."""

    title: str
    amount: float = Field(gt=0)
    category: str
    date: date_type

    @field_validator("title", "category")
    @classmethod
    def not_blank(cls, value: str) -> str:
        """Reject empty or whitespace-only strings for title/category."""
        if not value.strip():
            raise ValueError("must not be blank")
        return value


class Expense(ExpenseCreate):
    """A stored expense, including its server-assigned id."""

    id: int
