from sqlalchemy import Column, BigInteger, Integer, String, Date
from .base import Base

class Eleicao(Base):
    __tablename__ = "eleicao"

    cd_eleicao = Column(BigInteger, primary_key=True)
    nr_turno = Column(Integer, primary_key=True)
    ano_eleicao = Column(Integer, nullable=False)
    cd_tipo_eleicao = Column(Integer)
    nm_tipo_eleicao = Column(String)
    ds_eleicao = Column(String)
    dt_eleicao = Column(Date)
