from sqlalchemy import Column, BigInteger, Integer, String, ForeignKey, Numeric, Date, UniqueConstraint
from .base import Base

class NotaFiscal(Base):
    __tablename__ = "nota_fiscal"

    id_nota = Column(BigInteger, primary_key=True, autoincrement=True)
    sq_candidato = Column(BigInteger, ForeignKey("candidatura.sq_candidato"), nullable=True)
    cd_eleicao = Column(Integer, nullable=False)
    nr_candidato = Column(Integer, nullable=False)
    sg_uf = Column(String(2), nullable=False)
    nr_nota_fiscal = Column(String)
    nr_serie = Column(String)
    cpf_cnpj_emitente = Column(String)
    dt_emissao = Column(Date)
    vr_nota_fiscal = Column(Numeric(15, 2))
    nr_chave_acesso = Column(String)
    nm_url_acesso = Column(String)

    __table_args__ = (
        UniqueConstraint(
            "cd_eleicao",
            "nr_candidato",
            "sg_uf",
            "nr_nota_fiscal",
            "cpf_cnpj_emitente",
            name="uq_nota_fiscal",
        ),
    )

