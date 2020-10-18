from sqlalchemy import Column, Integer, DateTime, ForeignKey, String
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from enum  import Enum as PyEnum


Base = declarative_base()


class Event(PyEnum):
    new = 1
    full = 2


class LunarEvent(Base):
    __tablename__ = 'lunar_event'
    id = Column(Integer, primary_key=True)
    cycle = Column(Integer)
    event = Column(SQLEnum(Event))
    datetime = Column(DateTime)


class LunarMonth(Base):
    __tablename__ = 'lunar_month'
    id = Column(Integer, primary_key=True)
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
