from sqlalchemy import Column, BigInteger, String, Integer, ForeignKey, PrimaryKeyConstraint
from .base import Base

class RedeSocial(Base):
    __tablename__ = "rede_social"

    sq_candidato = Column(BigInteger, ForeignKey("candidatura.sq_candidato"), nullable=False)
    nr_ordem = Column(Integer, nullable=False)
    ds_url = Column(String)
    tipo_rede_social = Column(String)

    __table_args__ = (
        PrimaryKeyConstraint("sq_candidato", "nr_ordem"),
    )
