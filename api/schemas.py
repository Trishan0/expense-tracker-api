from pydantic import BaseModel
from enum import Enum
import datetime

class Category(str, Enum):
    GROCERIES = "Groceries"
    LEISURE = "Leisure"
    ELECTRONICS = "Electronics"
    UTILITIES = "Utilities"
    CLOTHING = "Clothing"
    HEALTH = "Health"
    OTHER = "Others"

class Expense(BaseModel):
    id: int
    category: Category
    amount: float
    description: str
    date: datetime.date