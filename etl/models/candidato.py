from sqlalchemy import Column, String, Date
from .base import Base

class Candidato(Base):
    __tablename__ = "candidato"

    nr_cpf_candidato = Column(String, primary_key=True)
    nm_candidato = Column(String, nullable=False)
    nm_urna_candidato = Column(String)
    dt_nascimento = Column(Date)
    ds_genero = Column(String)
    ds_grau_instrucao = Column(String)
    ds_estado_civil = Column(String)
    ds_ocupacao = Column(String)
    sg_uf_nascimento = Column(String(2))
    nm_municipio_nascimento = Column(String)
