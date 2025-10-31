from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlmodel import select
from api.db_functions import init_db, get_db
import api.db_models as db_models

router = APIRouter(prefix="/expenses", tags=["Expenses"])


@router.get("/")
def get_all_expenses(db:Session = Depends(get_db)):
    db_expenses = db.query(db_models.Expense).all()
    return db_expenses
    


