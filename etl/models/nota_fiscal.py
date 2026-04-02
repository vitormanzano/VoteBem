from sqlalchemy import Column, BigInteger, String, Integer, ForeignKey, Numeric, Date
from .base import Base

class NotaFiscal(Base):
    __tablename__ = "nota_fiscal"

    id_nota = Column(BigInteger, primary_key=True)
    sq_candidato = Column(BigInteger, ForeignKey("candidatura.sq_candidato"))
    nr_nota_fiscal = Column(String)
    nm_fornecedor = Column(String)
    cd_tipo_despesa = Column(String)
    vr_despesa = Column(Numeric(15, 2))
    dt_despesa = Column(Date)
