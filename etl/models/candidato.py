from sqlalchemy import Column, String, Integer, Date
from .base import Base

class Candidato(Base):
    __tablename__ = "candidato"

    nr_cpf_candidato = Column(String(11), primary_key=True)
    nm_candidato = Column(String, nullable=False)
    nm_social_candidato = Column(String)
    nm_urna_candidato = Column(String)
    dt_nascimento = Column(Date)
    sg_uf_nascimento = Column(String(2))
    cd_genero = Column(Integer)
    ds_genero = Column(String)
    cd_grau_instrucao = Column(Integer)
    ds_grau_instrucao = Column(String)
    cd_estado_civil = Column(Integer)
    ds_estado_civil = Column(String)
    cd_cor_raca = Column(Integer)
    ds_cor_raca = Column(String)
