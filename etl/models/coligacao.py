from sqlalchemy import Column, BigInteger, Integer, ForeignKey, String 
from .base import Base

class Coligacao(Base):
    __tablename__ = "coligacao"
    sq_coligacao = Column(BigInteger, primary_key=True)
    nr_eleicao = Column(Integer, ForeignKey("eleicao.nr_eleicao")) 
    nm_coligacao = Column(String)
    sg_uf = Column(String(2))
    tp_agremiacao = Column(String)
