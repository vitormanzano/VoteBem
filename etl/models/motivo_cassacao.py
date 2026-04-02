from sqlalchemy import Column, BigInteger, String, Integer, ForeignKey, Date
from .base import Base

class MotivoCassacao(Base):
    __tablename__ = "motivo_cassacao"

    id_cassacao = Column(BigInteger, primary_key=True)
    sq_candidato = Column(BigInteger, ForeignKey("candidatura.sq_candidato"))
    cd_motivo = Column(String)
    ds_motivo = Column(String)
    dt_decisao = Column(Date)
    ds_orgao = Column(String)
