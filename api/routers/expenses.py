from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlmodel import select
from api.db_functions import init_db, get_db
import api.db_models as db_models
import api.models as models
import logging
from api.security import get_current_user
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/expenses", tags=["Expenses"])


@router.get("/")
def get_all_expenses(filter: str| None = None, start_date: str| None = None, end_date: str| None = None, db:Session = Depends(get_db), current_user:db_models.User = Depends(get_current_user)):
    query = db.query(db_models.Expense).filter(db_models.Expense.user_id == current_user.id)
    
    if filter is None:
        pass
    elif filter =="last_week":
        last_week = datetime.now() - timedelta(days=7)
        query = query.filter(db_models.Expense.date >= last_week)
        
    elif filter =="last_month":
        last_month = datetime.now() - timedelta(days=30)
        query = query.filter(db_models.Expense.date >= last_month)
        
    elif filter =="last_3_months":
        last_three_months = datetime.now() - timedelta(days=90)
        query = query.filter(db_models.Expense.date >= last_three_months)
        
    elif filter == "custom":
        if start_date is None or end_date is None:
            raise HTTPException(status_code=400, detail="start_date and end_date are required for custom filter")
        try:
            start_dt = datetime.fromisoformat(start_date)
            end_dt = datetime.fromisoformat(end_date)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD")

        if start_dt > end_dt:
            raise HTTPException(status_code=400, detail="start_date must be before end_date")
            
        query = query.filter(db_models.Expense.date >= start_dt, db_models.Expense.date <= end_dt)

    else:
        raise HTTPException(status_code=400, detail="Invalid filter value")
            
    db_expenses = query.all()
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