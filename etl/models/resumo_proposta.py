from sqlalchemy import Column, BigInteger, Text, DateTime, ForeignKey
from .base import Base

class ResumoProposta(Base):
    __tablename__ = "resumo_proposta"

    id_resumo = Column(BigInteger, primary_key=True)
    id_proposta = Column(BigInteger, ForeignKey("proposta_governo.id_proposta"))
    ds_tema = Column(Text)
    tx_resumo = Column(Text)
    dt_geracao = Column(DateTime)
