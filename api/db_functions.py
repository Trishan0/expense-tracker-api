from api.database import sessionLocal, engine
import api.models as models
import api.db_models as db_models
import json 
import pathlib

db_models.Base.metadata.create_all(bind=engine)

sample_data_path = pathlib.Path(__file__).with_name("sample_data.json")

with sample_data_path.open("r", encoding="utf-8")as sample_file:
    sample_data = json.load(sample_file)
expenses = [models.ExpenseCreate(**expense) for expense in sample_data]

def get_db():
    try:
        db = sessionLocal()
        yield db
    finally:
        db.close()
        

def init_db():
    db = sessionLocal()
    
    user_count = db.query(db_models.User).count()
    if user_count ==0:
        from api.security import hash_password
        
        test_user = db_models.User(username="test", password=hash_password("test"))
        db.add(test_user)
        db.commit()
        db.refresh(test_user)
        
        expense_count = db.query(db_models.Expense).count()
        if expense_count ==0:
            for expense in expenses:
                db_expense = db_models.Expense(**expense.model_dump(), user_id=test_user.id)
                db.add(db_expense)
    db.commit()
    db.close()

init_db()