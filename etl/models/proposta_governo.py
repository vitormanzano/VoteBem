from sqlalchemy import Column, BigInteger, String, Boolean, Text, DateTime, ForeignKey
from .base import Base

class PropostaGoverno(Base):
    __tablename__ = "proposta_governo"

    sq_candidato = Column(BigInteger, ForeignKey("candidatura.sq_candidato"), primary_key=True)
    nm_arquivo = Column(String)
    ds_caminho_arquivo = Column(String)
    tx_conteudo_extraido = Column(Text)
    st_processado = Column(Boolean, default=False)
    dt_processamento = Column(DateTime)
