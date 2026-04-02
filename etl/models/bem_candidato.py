from sqlalchemy import Column, BigInteger, String, Integer, ForeignKey, Numeric 
from .base import Base

class BemCandidato(Base):
    __tablename__ = "bem_candidato"

    id_bem = Column(BigInteger, primary_key=True)
    sq_candidato = Column(BigInteger, ForeignKey("candidatura.sq_candidato"))
    nr_ordem_bem = Column(Integer)
    cd_tipo_bem = Column(String)
    ds_tipo_bem = Column(String)
    vr_bem = Column(Numeric(15, 2))
