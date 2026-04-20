from sqlalchemy import Column, BigInteger, String, Integer, ForeignKey, Numeric, PrimaryKeyConstraint
from .base import Base

class BemCandidato(Base):
    __tablename__ = "bem_candidato"

    sq_candidato = Column(BigInteger, ForeignKey("candidatura.sq_candidato"), nullable=False)
    nr_ordem_bem = Column(Integer, nullable=False)
    cd_tipo_bem = Column(Integer)
    ds_tipo_bem = Column(String)
    ds_bem = Column(String)
    vr_bem = Column(Numeric(15, 2))

    __table_args__ = (
        PrimaryKeyConstraint("sq_candidato", "nr_ordem_bem"),
    )
