from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import incident as models
from app.schemas import incident as schemas

router = APIRouter()

@router.get("/incidents", response_model=list[schemas.IncidentRead])
def get_incidents(db: Session = Depends(get_db)):
    incidents = db.query(models.Incident).all()
    return incidents

@router.post("/incidents", response_model=schemas.IncidentRead)
def create_incident(incident: schemas.IncidentCreate, db: Session = Depends(get_db)):
    db_incident = models.Incident(**incident.dict())
    db.add(db_incident)
    db.commit()
    db.refresh(db_incident)
    return db_incident