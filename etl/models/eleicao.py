from sqlalchemy import Column, Integer, String, Date
from .base import Base

class Eleicao(Base):
    __tablename__ = "eleicao"

    nr_eleicao = Column(Integer, primary_key=True)
    ds_eleicao = Column(String, nullable=False)
    cd_tipo_eleicao = Column(String)
    dt_eleicao = Column(Date)
