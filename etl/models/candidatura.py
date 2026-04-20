from sqlalchemy import Column, BigInteger, String, Integer, ForeignKey, Numeric
from .base import Base

class Candidatura(Base):
    __tablename__ = "candidatura"

    sq_candidato = Column(BigInteger, primary_key=True)
    nr_cpf_candidato = Column(String(11), ForeignKey("candidato.nr_cpf_candidato"), nullable=False)
    cd_eleicao = Column(BigInteger, nullable=False)
    nr_partido = Column(Integer, ForeignKey("partido.nr_partido"))
    sq_coligacao = Column(BigInteger, ForeignKey("coligacao.sq_coligacao"))
    nm_urna_candidato = Column(String)
    cd_cargo = Column(Integer)
    ds_cargo = Column(String)
    sg_uf = Column(String(2))
    nr_candidato = Column(Integer)
    cd_situacao_candidatura = Column(Integer)
    ds_situacao_candidatura = Column(String)
    cd_ocupacao = Column(Integer)
    ds_ocupacao = Column(String)
    foto_url = Column(String)
    st_reeleicao = Column(String(1))
    vr_despesa_max_campanha = Column(Numeric(15, 2))
