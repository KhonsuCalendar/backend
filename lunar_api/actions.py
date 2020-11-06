from datetime import datetime
from typing import Optional

from sqlalchemy.orm import Session
from . import models, schemas


def add_lunar_event(db: Session, lunar_event: schemas.LunarEventCreate):
    event = models.LunarEvent(**lunar_event.dict())
    db.add(event)
    db.commit()
    db.refresh(event)
    return event


def get_lunar_events(db: Session, start_date: Optional[datetime] = None, end_date: Optional[datetime] = None):
    query = db.query(models.LunarEvent)
    if start_date:
        query = query.filter(models.LunarEvent.datetime >= start_date)
    if end_date:
        query = query.filter(models.LunarEvent.datetime <= end_date)
    return query.all()


def get_phase_for_day(db, date):
    query = db.query(models.LunarEvent).filter(models.LunarEvent.datetime == date)
    try:
        query = query.all()[0]
        return query.phase
    except IndexError:
        return ''
