from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlmodel import select
from api.db_functions import init_db, get_db
import api.db_models as db_models
import api.models as models
router = APIRouter(prefix="/expenses", tags=["Expenses"])


@router.get("/")
def get_all_expenses(db:Session = Depends(get_db)):
    db_expenses = db.query(db_models.Expense).all()
    return db_expenses
    

@router.get("/{expense_id}")
def get_expense_by_id(expense_id:int, db:Session = Depends(get_db)):
    expense = db.query(db_models.Expense).filter(db_models.Expense.id == expense_id).first()
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    return expense

@router.post("/")
def create_expense(expense:models.ExpenseBase, db:Session = Depends(get_db)):
    db.add(db_models.Expense(**expense.model_dump()))
    db.commit()
    print("Expense created successfully")
    return expense

@router.put("/{expense_id}")
def update_expense(expense_id:int, updated_expense: models.ExpenseBase, db:Session = Depends(get_db)):
    expense = db.query(db_models.Expense).filter(db_models.Expense.id == expense_id).first()
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    expense.description = updated_expense.description
    expense.amount = updated_expense.amount
    expense.date = updated_expense.date
    expense.category = updated_expense.category
    db.commit()
    
    return {"message": "Expense updated successfully"}
 
@router.delete("/{expense_id}")
def delete_expense(expense_id:int, db:Session = Depends(get_db)):
    expense = db.query(db_models.Expense).filter(db_models.Expense.id == expense_id).first()
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    db.delete(expense)
    db.commit()
    return {"message": "Expense deleted successfully"}