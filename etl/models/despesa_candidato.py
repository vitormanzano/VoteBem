from sqlalchemy import Column, BigInteger, String, ForeignKey, Numeric, Date, Text, UniqueConstraint
from .base import Base

class DespesaCandidato(Base):
    __tablename__ = "despesa_candidato"

    id_despesa = Column(BigInteger, primary_key=True, autoincrement=True)
    sq_candidato = Column(BigInteger, ForeignKey("candidatura.sq_candidato"), nullable=False)
    nr_documento = Column(String)
    cpf_cnpj_fornecedor = Column(String)
    nm_fornecedor = Column(String)
    dt_despesa = Column(Date)
    vr_despesa = Column(Numeric(15, 2))
    ds_tipo_despesa = Column(String)
    ds_fonte_recurso = Column(String)
    ds_especie_recurso = Column(String)
    ds_despesa = Column(Text)

    __table_args__ = (
        UniqueConstraint("sq_candidato", "nr_documento", "cpf_cnpj_fornecedor", "dt_despesa"),
    )
