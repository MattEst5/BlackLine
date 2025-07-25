from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import incident as models
from app.schemas import incident as schemas
from typing import Optional

router = APIRouter()

@router.get("/incidents/search", response_model=list[schemas.IncidentRead])
def search_incidents(
    department_id: Optional[int] = None,
    station_id: Optional[int] = None,
    incident_type: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(models.Incident)

    if department_id:
        query = query.filter(models.Incident.department_id == department_id)
    if station_id:
        query = query.filter(models.Incident.station_id == station_id)
    if incident_type:
        query = query.filter(models.Incident.incident_type == incident_type)

    return query.all()

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

@router.get("/incidents/{incident_id}", response_model=schemas.IncidentRead)
def get_incident(incident_id: int, db: Session = Depends(get_db)):
    incident = db.query(models.Incident).filter(models.Incident.incident_id == incident_id).first()
    if incident is None:
        raise HTTPException(status_code=404, detail="Incident not found")
    return incident

@router.delete("/incidents/{incident_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_incident(incident_id: int, db: Session = Depends(get_db)):
    incident = db.query(models.Incident).filter(models.Incident.incident_id == incident_id).first()
    if incident is None:
        raise HTTPException(status_code=404, detail="Incident not found")
    
    db.delete(incident)
    db.commit()
    return

@router.patch("/incidents/{incident_id}", response_model=schemas.IncidentRead)
def update_incident(incident_id: int, updated_data: schemas.IncidentCreate, db: Session = Depends(get_db)):
    incident = db.query(models.Incident).filter(models.Incident.incident_id == incident_id).first()
    if incident is None:
        raise HTTPException(status_code=404, detail="Incident not found")
    
    for key, value in updated_data.dict(exclude_unset=True).items():
        setattr(incident, key, value)

    db.commit()
    db.refresh(incident)
    return incident