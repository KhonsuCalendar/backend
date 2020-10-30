from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel


class LunarEventBase(BaseModel):
    cycle: int
    datetime: datetime
    phase: str


class LunarEventCreate(LunarEventBase):
    pass


class LunarEvent(LunarEventBase):
    id: int

    class Config:
        orm_mode = True
