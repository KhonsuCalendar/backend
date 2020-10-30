from sqlalchemy import Column, Integer, DateTime, ForeignKey, Unicode
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


Base = declarative_base()


class Phase(Base):
    __tablename__ = 'phases'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(Unicode)


class LunarEvent(Base):
    __tablename__ = 'lunar_event'

    id = Column(Integer, primary_key=True)
    cycle = Column(Integer)
    datetime = Column(DateTime)
    phase = Column(Unicode)
    # phase_id = Column(Integer, ForeignKey("phases.id"))
    #
    # phase = relationship("Phase")


class LunarMonth(Base):
    __tablename__ = 'lunar_month'
    id = Column(Integer, primary_key=True)
    # Should this specifically be the full moon event of the month or something?
    event_id = Column(Integer, ForeignKey(LunarEvent.id))
    event = relationship(LunarEvent)
    month = Column(Integer)
    name = Column(Unicode)
    start_date = Column(DateTime)
    end_date = Column(DateTime)


class Day(Base):
    __tablename__ = 'day'
    id = Column(Integer, primary_key=True)
    date = Column(DateTime)
    event_id = Column(Integer, ForeignKey(LunarEvent.id))
    event = relationship(LunarEvent)
