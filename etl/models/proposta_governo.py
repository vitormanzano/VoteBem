from sqlalchemy import Column, BigInteger, String, Boolean, Text, DateTime, ForeignKey
from .base import Base

class PropostaGoverno(Base):
    __tablename__ = "proposta_governo"

    id_proposta = Column(BigInteger, primary_key=True)
    sq_candidato = Column(BigInteger, ForeignKey("candidatura.sq_candidato"))
    nm_arquivo = Column(String, nullable=False)
    ds_caminho_arquivo = Column(String)
    tx_conteudo_extraido = Column(Text)
    st_processado = Column(Boolean, default=False)
    dt_processamento = Column(DateTime)
