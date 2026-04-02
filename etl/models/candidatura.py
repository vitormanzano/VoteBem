from sqlalchemy import Column, BigInteger, String, Integer, ForeignKey
from .base import Base

class Candidatura(Base):
    __tablename__ = "candidatura"

    sq_candidato = Column(BigInteger, primary_key=True)
    nr_cpf_candidato = Column(String, ForeignKey("candidato.nr_cpf_candidato"))
    nr_eleicao = Column(Integer, ForeignKey("eleicao.nr_eleicao"))
    nr_partido = Column(Integer, ForeignKey("partido.nr_partido"))
    sq_coligacao = Column(BigInteger, ForeignKey("coligacao.sq_coligacao"))
    nm_urna_candidato = Column(String)
    cd_cargo = Column(String)
    ds_cargo = Column(String)
    sg_uf = Column(String)
    nr_candidato = Column(Integer)
    cd_situacao_candidatura = Column(String)
    ds_situacao_candidatura = Column(String)
    nr_votos = Column(BigInteger)
    cd_sit_tot_turno = Column(String)
    

