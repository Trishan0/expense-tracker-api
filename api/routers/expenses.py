from fastapi import APIRouter
from api.schemas import Expense
from fastapi import HTTPException

router = APIRouter(prefix="/expenses", tags=["Expenses"])

db_expenses: list[Expense] = []

@router.get("/", response_model=list[Expense])
def get_expenses():
    return db_expenses

@router.get("/{expense_id}", response_model=Expense)
def get_expense_by_id(expense_id:int):
    for expense in db_expenses:
        if expense.id == expense_id:
            return expense
    raise HTTPException(status_code=404, detail="Task not found")

@router.post("/", response_model=Expense)
def create_expense(expense:Expense):
    for existing_expense in db_expenses:
        if expense.id == existing_expense.id:
            raise HTTPException(status_code=400, detail="Expense with this ID already exists")
    db_expenses.append(expense)
    return expense

@router.put("/{expense_id}", response_model=Expense)
def update_expense(expense_id:int, expense:Expense):
    for idx, existing_expense in enumerate(db_expenses):
        if existing_expense.id == expense_id:
            updated_expense = existing_expense.model_copy(update=expense.model_dump(exclude_unset=True))
            db_expenses[idx] = updated_expense
            return updated_expense
    raise HTTPException(status_code=404, detail="Expense not found")

@router.delete("/{expense_id}", response_model=Expense)
def delete_expense(expense_id:int):
    for idx, existing_expense in enumerate(db_expenses):
        if existing_expense.id == expense_id:
            return db_expenses.pop(idx)
    raise HTTPException(status_code=404, detail="Expense not found")