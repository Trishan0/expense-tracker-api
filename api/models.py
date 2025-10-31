from pydantic import BaseModel

class ExpenseBase(BaseModel):
    id: int
    description: str
    amount: float
    date: str
    category: str