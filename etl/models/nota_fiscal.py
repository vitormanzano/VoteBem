from sqlalchemy import Column, BigInteger, String, ForeignKey, Numeric, Date, UniqueConstraint
from .base import Base

class NotaFiscal(Base):
    __tablename__ = "nota_fiscal"

    id_nota = Column(BigInteger, primary_key=True, autoincrement=True)
    sq_candidato = Column(BigInteger, ForeignKey("candidatura.sq_candidato"), nullable=False)
    nr_nota_fiscal = Column(String)
    nr_serie = Column(String)
    cpf_cnpj_emitente = Column(String)
    dt_emissao = Column(Date)
    vr_nota_fiscal = Column(Numeric(15, 2))
    nr_chave_acesso = Column(String)
    nm_url_acesso = Column(String)

    __table_args__ = (
        UniqueConstraint("sq_candidato", "nr_nota_fiscal", "cpf_cnpj_emitente"),
    )
