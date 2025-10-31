from api.database import sessionLocal, engine
import api.models as models
import api.db_models as db_models
import json 
import pathlib

db_models.Base.metadata.create_all(bind=engine)

sample_data_path = pathlib.Path(__file__).with_name("sample_data.json")

with sample_data_path.open("r", encoding="utf-8")as sample_file:
    sample_data = json.load(sample_file)
expenses = [models.ExpenseBase(**expense) for expense in sample_data]

def get_db():
    try:
        db = sessionLocal()
        yield db
    finally:
        db.close()
        

def init_db():
    db = sessionLocal()
    count = db.query(db_models.Expense).count()
    if count ==0:
        for expense in expenses:
            db.add(db_models.Expense(**expense.model_dump()))
    db.commit()

init_db()