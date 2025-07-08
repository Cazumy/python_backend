from sqlalchemy import Column, Integer, Float, Date
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Roll(Base):
    __tablename__ = 'rolls'
    
    id = Column(Integer, primary_key=True, index=True)
    length = Column(Float, nullable=False)
    weight = Column(Float, nullable=False)
    date_of_adding = Column(Date, nullable=True)
    date_of_removing = Column(Date, nullable=True)