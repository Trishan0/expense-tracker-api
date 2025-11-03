from sqlalchemy import Column, Integer, String,  Float, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Expense(Base):
    __tablename__ = "expense"
    
    id = Column(Integer, primary_key=True, index=True)
    description = Column(String)
    amount = Column(Float)
    date = Column(DateTime)
    category = Column(String)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    
    user = relationship("User", back_populates="expenses")
    
    
class User(Base):
    __tablename__ = "user"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String(100))
    
    expenses = relationship("Expense", back_populates="user")
    