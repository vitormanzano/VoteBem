from sqlalchemy import Column, BigInteger, String, ForeignKey, PrimaryKeyConstraint
from .base import Base

class MotivoCassacao(Base):
    __tablename__ = "motivo_cassacao"

    sq_candidato = Column(BigInteger, ForeignKey("candidatura.sq_candidato"), nullable=False)
    ds_tp_motivo = Column(String)
    ds_motivo = Column(String, nullable=False)

    __table_args__ = (
        PrimaryKeyConstraint("sq_candidato", "ds_motivo"),
    )
