from sqlalchemy import Column, BigInteger, String, Text, DateTime, ForeignKey, func
from .base import Base

class ResumoProposta(Base):
    __tablename__ = "resumo_proposta"

    id_resumo = Column(BigInteger, primary_key=True, autoincrement=True)
    sq_candidato = Column(BigInteger, ForeignKey("proposta_governo.sq_candidato"), nullable=False)
    ds_tema = Column(String, nullable=False)
    tx_resumo = Column(Text, nullable=False)
    dt_geracao = Column(DateTime, server_default=func.current_timestamp())
