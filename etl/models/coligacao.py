from sqlalchemy import Column, BigInteger, Integer, String, ForeignKeyConstraint
from .base import Base

class Coligacao(Base):
    __tablename__ = "coligacao"

    sq_coligacao = Column(BigInteger, primary_key=True)
    cd_eleicao = Column(BigInteger, nullable=False)
    nr_turno = Column(Integer, nullable=False)
    nm_coligacao = Column(String)
    ds_composicao_coligacao = Column(String)
    tp_agremiacao = Column(String)
    sg_uf = Column(String(2))

    __table_args__ = (
        ForeignKeyConstraint(
            ["cd_eleicao", "nr_turno"],
            ["eleicao.cd_eleicao", "eleicao.nr_turno"]
        ),
    )
