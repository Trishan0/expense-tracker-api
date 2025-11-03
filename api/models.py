from pydantic import BaseModel
import datetime

class UserRegister(BaseModel):
    username: str
    password: str
    confirm_password: str
    
class UserLogin(BaseModel):
    username: str
    password: str


class UserResponse(BaseModel):
    id: int
    username: str

    class Config:
        from_attributes = True

class ExpenseCreate(BaseModel):
    description: str
    amount: float
    date: datetime.date
    category: str
    
class ExpenseUpdate(BaseModel):
    description: str | None = None
    amount: float | None = None
    date: datetime.date | None = None
    category: str | None = None
    
class ExpenseResponse(BaseModel):
    id: int
    description: str
    amount: float
    date: datetime.date
    category: str
    user_id: int
    
    class Config:
        from_attributes = True