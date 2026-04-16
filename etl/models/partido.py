from sqlalchemy import Column, Integer, String 
from .base import Base

class Partido(Base):
    __tablename__ = "partido"

    nr_partido = Column(Integer, primary_key=True)
    sg_partido = Column(String(20), nullable=False)
    nm_partido = Column(String, nullable=False)
