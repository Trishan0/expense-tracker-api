from sqlalchemy import Column, Integer, String,  Float, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Expense(Base):
    __tablename__ = "expense"
    
    id = Column(Integer, primary_key=True, index=True)
    description = Column(String)
    amount = Column(Float)
    date = Column(DateTime)
    category = Column(String)