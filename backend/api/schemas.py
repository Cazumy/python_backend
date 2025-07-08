from datetime import date
from pydantic import BaseModel
from typing import Optional

class RollCreate(BaseModel):
    length: float
    weight: float
    date_of_adding: Optional[date] = None
    date_of_removing: Optional[date] = None

class RollRead(RollCreate):
    id: int

    class Config:
        orm_mode = True