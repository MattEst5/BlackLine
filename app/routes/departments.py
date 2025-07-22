from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import department as models
from app.schemas import department as schemas
from app.utils.auth_handler import get_current_user
from app.utils.role_checker import require_admin

router = APIRouter()

@router.post("/departments", response_model=schemas.DepartmentRead, status_code=status.HTTP_201_CREATED)
def create_department(dept: schemas.DepartmentCreate, db: Session = Depends(get_db), current_user = Depends(require_admin)):
    existing_dept = db.query(models.Department).filter(models.Department.name == dept.name).first
    if existing_dept:
        raise HTTPException(status_code=400, detail="Department already exists.")
    
    new_dept = models.Department(name=dept.name)
    db.add(new_dept)
    db.commit()
    db.refresh(new_dept)
    return new_dept

@router.get("/departments", response_model=list[schemas.DepartmentRead])
def read_departments(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return db.query(models.Department).all()

@router.patch("/departments/{dept_id}", response_model=schemas.DepartmentRead)
def update_department(dept_id: int, dept_update: schemas.DepartmentUpdate, db: Session = Depends(get_db), current_user = Depends(require_admin)):
    dept = db.query(models.Department).filter(models.Department.dept_id == dept_id).first()
    if not dept:
        raise HTTPException(status_code=404, detail="Department not found.")
    
    dept.name = dept_update.name
    db.commit()
    db.refresh(dept)
    return dept

@router.delete("/departments/{dept_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_department(dept_id: int, db: Session = Depends(get_db), current_user = Depends(require_admin)):
    dept = db.query(models.Department).filter(models.Department.dept_id == dept_id).first()
    if not dept:
        raise HTTPException(status_code=404, detail="Department not found.")
    
    db.delete(dept)
    db.commit()
    return None
