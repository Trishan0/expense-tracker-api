from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from api.db_functions import get_db
import api.db_models as db_models
import api.models as models
from api.security import hash_password, verify_password, create_access_token

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=models.UserResponse, status_code=status.HTTP_201_CREATED,)
def register_user(user: models.UserRegister, db: Session = Depends(get_db)):
    existing_user = db.query(db_models.User).filter(db_models.User.username == user.username).first()
    
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exists")
    
    if user.password != user.confirm_password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Passwords do not match")
    
    hashed_password = hash_password(user.password)
    
    new_user = db_models.User(username=user.username, password=hashed_password)
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user