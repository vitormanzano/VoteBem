from sqlalchemy import Column, BigInteger, String, Integer, ForeignKey, Date
from .base import Base


class CertidaoCriminal(Base):
    __tablename__ = "certidao_criminal"

    id_certidao = Column(BigInteger, primary_key=True)
    sq_candidato = Column(BigInteger, ForeignKey("candidatura.sq_candidato"))
    nm_arquivo = Column(String, nullable=False)
    ds_caminho_arquivo = Column(String)
    dt_emissao = Column(Date)
    dt_validade = Column(Date)
