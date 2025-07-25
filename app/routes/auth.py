from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import user as models
from app.schemas import auth as schemas
from app.utils import auth as utils
from app.utils.role_checker import require_admin

router = APIRouter()

@router.post("/login", response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == form_data.username).first()
    if not user or not utils.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    
    access_token = utils.create_access_token({"user_id": user.user_id})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/admin-only")
def read_admin_data(current_user = Depends(require_admin)):
    return {"message": f"Welcome, {current_user.username}. You have admin access."}
