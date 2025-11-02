from pydantic import BaseModel
from datetime import date

class ExpenseBase(BaseModel):
    id: int
    description: str
    amount: float
    date: date
    category: str
    
class ExpenseUpdate(BaseModel):
    description: str | None = None
    amount: float | None = None
    date: date | None = None
    category: str | None = None