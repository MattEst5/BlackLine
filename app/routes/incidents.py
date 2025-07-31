from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime, date
from app.database import get_db
from app.models import incident as models
from app.models import shift as shift_models
from app.models import incident_personnel as personnel_models
from app.schemas import incident as schemas
from app.utils import auth_handler
from typing import Optional

router = APIRouter()

@router.get("/incidents/search", response_model=list[schemas.IncidentRead])
def search_incidents(
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    station_id: Optional[int] = None,
    incident_type: Optional[str] = None,
    shift_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    query = db.query(models.Incident)

    # Convert date-only inputs to datetime bounds
    start_dt = None
    end_dt = None
    if start_date:
        start_dt = datetime.combine(start_date, datetime.min.time())
    if end_date:
        end_dt = datetime.combine(end_date, datetime.max.time())

    # Validation: ensure start_date <= end_date
    if start_dt and end_dt and start_dt > end_dt:
        raise HTTPException(
            status_code=400,
            detail="Start date cannot be after end date."
        )
    
    # Apply date filters
    if start_dt and end_dt:
        query = query.filter(models.Incident.call_time.between(start_dt, end_dt))
    elif start_dt:
        query = query.filter(models.Incident.call_time >= start_dt)
    elif end_dt:
        query = query.filter(models.Incident.call_time <= end_dt)

    # Other filters
    if station_id:
        query = query.filter(models.Incident.station_id == station_id)
    if incident_type:
        query = query.filter(models.Incident.incident_type == incident_type)
    if shift_id:
        query = query.filter(models.Incident.shift_id == shift_id)

    return query.all()

@router.get("/incidents", response_model=list[schemas.IncidentRead])
def get_incidents(db: Session = Depends(get_db)):
    incidents = db.query(models.Incident).all()
    return incidents

@router.post("/incidents", response_model=schemas.IncidentRead, status_code=status.HTTP_201_CREATED)
def create_incident(incident: schemas.IncidentCreate,
                    db: Session = Depends(get_db),
                    current_user = Depends(auth_handler.get_current_user)):
    
    #Create new incident
    db_incident = models.Incident(
        dept_id=current_user.dept_id,
        shift_id=incident.shift_id,
        incident_number=incident.incident_number,
        alarm_time=incident.alarm_time or datetime.utcnow(),
        business_name=incident.business_name,
        address=incident.address,
        city=incident.city,
        state=incident.state,
        zipcode=incident.zipcode,
        latitude=incident.latitude,
        longitude=incident.longitude,
        narrative=incident.narrative,
        mutual_aid=incident.mutual_aid
    )
    db.add(db_incident)
    db.commit()
    db.refresh(db_incident)

    #Grab today's shift roster
    today = date.today()
    shift_roster = db.query(shift_models.ShiftRoster).filter(
        shift_models.ShiftRoster.shift_date == today,
        shift_models.ShiftRoster.shift_id == incident.shift_id).all()
    
    #Insert personnel from shift_rosters into incident_personnel
    for roster_entry in shift_roster:
        db_personnel = personnel_models.IncidentPersonnel(
            incident_id=db_incident.incident_id,
            user_id=roster_entry.user_id,
            unit_id=roster_entry.unit_id,
            unit_task=roster_entry.unit_task,
        )
        db.add(db_personnel)

    db.commit()
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