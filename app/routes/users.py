from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import user as models
from app.schemas import user as schemas
from app.utils import auth as utils, auth_handler

router = APIRouter()

@router.post("/users", response_model=schemas.UserRead, status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    #Check if username already exists
    existing_user = db.query(models.User).filter(models.User.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    hashed_pw = utils.hash_password(user.password)
    db_user = models.User(
        dept_id=user.dept_id,
        username=user.username,
        hashed_password=hashed_pw,
        full_name=user.full_name,
        email=user.email
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.get("/users/me", response_model=schemas.UserRead)
def read_users_me(current_user: models.User = Depends(auth_handler.get_current_user)):
    return current_user