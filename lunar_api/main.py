from datetime import datetime
from typing import Optional, List

import uvicorn
from fastapi import FastAPI
from fastapi import Depends
from sqlalchemy.orm import Session

from lunar_api import actions
from lunar_api import schemas
from lunar_api.database import SessionLocal


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


app = FastAPI()


@app.get("/")
async def root():
    return {'message': 'hello, world'}


@app.post("/event/", response_model=schemas.LunarEvent)
async def create_lunar_event(item: schemas.LunarEventCreate, db: Session = Depends(get_db)):
    if not item.datetime:
        raise(ValueError, 'Item must have a datettime in ISO format')
    if item.cycle is None:
        raise(ValueError, 'Item must have a cycle, generally the date of the new moon')
    if not item.phase:
        raise(ValueError, 'Item must have a phase, string format')
    return actions.add_lunar_event(db, item)


@app.get("/events/", response_model=List[schemas.LunarEvent])
def get_lunar_events(start_date: Optional[datetime] = None, end_date: Optional[datetime] = None, db: Session = Depends(get_db)):
    lunar_events = actions.get_lunar_events(db, start_date, end_date)
    return lunar_events


if __name__ == '__main__':
    uvicorn.run("main:app", host='0.0.0.0', port=8000, reload=True)