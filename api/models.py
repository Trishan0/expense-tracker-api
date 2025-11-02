from pydantic import BaseModel
import datetime

class ExpenseBase(BaseModel):
    id: int
    description: str
    amount: float
    date: datetime.date
    category: str
    
class ExpenseUpdate(BaseModel):
    description: str | None = None
    amount: float | None = None
    date: datetime.date | None = None
    category: str | None = None