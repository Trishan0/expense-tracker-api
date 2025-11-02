from pydantic import BaseModel

class ExpenseBase(BaseModel):
    id: int
    description: str
    amount: float
    date: str
    category: str
    
class ExpenseUpdate(BaseModel):
    description: str | None = None
    amount: float | None = None
    date: str | None = None
    category: str | None = None