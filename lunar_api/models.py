from sqlalchemy import Column, Integer, DateTime, ForeignKey, String
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.orm import relationship

from .database import Base


class Phase(Base):
    __tablename__ = 'phases'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)


class LunarEvent(Base):
    __tablename__ = 'lunar_event'

    id = Column(Integer, primary_key=True)
    cycle = Column(Integer)
    datetime = Column(DateTime)
    phase_id = Column(Integer, ForeignKey("phases.id"))

    phase = relationship("Phase")


class LunarMonth(Base):
    __tablename__ = 'lunar_month'
    id = Column(Integer, primary_key=True)
    # Should this specifically be the full moon event of the month or something?
    event_id = Column(Integer, ForeignKey(LunarEvent.id))
    event = relationship(LunarEvent)
    month = Column(Integer)
    name = Column(String)


class Day(Base):
    __tablename__ = 'day'
    id = Column(Integer, primary_key=True)
    date = Column(DateTime)
    event_id = Column(Integer, ForeignKey(LunarEvent.id))
    event = relationship(LunarEvent)
