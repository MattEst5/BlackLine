from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import user as models
from app.schemas import user as schemas
from app.utils import auth as utils, auth_handler
from app.utils.role_checker import require_admin

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

@router.get("/users", response_model=list[schemas.UserRead])
def read_users(db: Session = Depends(get_db), current_user = Depends(require_admin)):
    users = db.query(models.User).all()
    return users

@router.get("/users/me", response_model=schemas.UserRead)
def read_users_me(current_user: models.User = Depends(auth_handler.get_current_user)):
    return current_user

@router.patch("/users/{user_id}", response_model=schemas.UserRead)
def update_user(user_id: int, user_update: schemas.UserUpdate,
                db: Session = Depends(get_db),
                current_user= Depends(require_admin)):
    user = db.query(models.User).filter(models.User.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if user_update.full_name is not None:
        user.full_name = user_update.full_name
    if user_update.email is not None:
        user.emain = user_update.email
    if user_update.role is not None:
        user.role = user_update.role

    db.commit()
    db.refresh(user)
    return user

@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Session = Depends(get_db),
                current_user = Depends(require_admin)):
    user = db.query(models.User).filter(models.User.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    db.delete(user)
    db.commit()
    return
