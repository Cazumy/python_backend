from datetime import date
from pydantic import BaseModel

class RollCreate(BaseModel):
    length: float
    weight: float
    date_of_adding: date = None
    date_of_removing: date = None

class RollRead(RollCreate):
    id: int

    class Config:
        orm_mode = True