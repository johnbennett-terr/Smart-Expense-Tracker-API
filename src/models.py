from datetime import date as date_type

from pydantic import BaseModel, Field, field_validator


class ExpenseCreate(BaseModel):
    title: str
    amount: float = Field(gt=0)
    category: str
    date: date_type

    @field_validator("title", "category")
    @classmethod
    def not_blank(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("must not be blank")
        return value


class Expense(ExpenseCreate):
    id: int
