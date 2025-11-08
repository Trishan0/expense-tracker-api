from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlmodel import select
from api.db_functions import init_db, get_db
import api.db_models as db_models
import api.models as models
import logging
from api.security import get_current_user

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/expenses", tags=["Expenses"])


@router.get("/")
def get_all_expenses(db:Session = Depends(get_db), current_user:db_models.User = Depends(get_current_user)):
    db_expenses = db.query(db_models.Expense).filter(db_models.Expense.user_id == current_user.id).all()
    return db_expenses
    

@router.get("/{expense_id}")
def get_expense_by_id(expense_id:int, db:Session = Depends(get_db), current_user: db_models.User = Depends(get_current_user)):
    expense = db.query(db_models.Expense).filter(db_models.Expense.id == expense_id, db_models.Expense.user_id == current_user.id).first()
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    return expense

@router.post("/")
def create_expense(expense:models.ExpenseCreate, db:Session = Depends(get_db), current_user:db_models.User = Depends(get_current_user)):
    db_expense = db_models.Expense(**expense.model_dump(),user_id = current_user.id)
    db.add(db_expense)
    db.commit()
    db.refresh(db_expense)  
    logger.info(f"Created expense with ID: {db_expense.id}")
    return db_expense

@router.patch("/{expense_id}")
def partial_update_expense(expense_id: int, updated_fields: models.ExpenseUpdate, db: Session = Depends(get_db), current_user:db_models.User= Depends(get_current_user)):
    expense = db.query(db_models.Expense).filter(db_models.Expense.id == expense_id, db_models.Expense.user_id == current_user.id).first()
    
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    
    update_dict = updated_fields.model_dump(exclude_unset=True)
    
    for key, value in update_dict.items():
        setattr(expense, key, value)
        
    db.commit()
    db.refresh(expense)
    logger.info(f"Partially updated expense with ID: {expense.id}")
    return expense
    
    
 
@router.delete("/{expense_id}")
def delete_expense(expense_id:int, db:Session = Depends(get_db), current_user:db_models.User = Depends(get_current_user)):
    expense = db.query(db_models.Expense).filter(db_models.Expense.id == expense_id, db_models.Expense.user_id == current_user.id).first()
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    db.delete(expense)
    db.commit()
    logger.info(f"Deleted expense with ID: {expense.id}")
    return {"message": "Expense deleted successfully"}