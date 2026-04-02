from sqlalchemy import Column, BigInteger, String, Integer, ForeignKey
from .base import Base

class RedeSocial(Base):
    __tablename__ = "rede_social"

    id_rede_social = Column(BigInteger, primary_key=True)
    sq_candidato = Column(BigInteger, ForeignKey("candidatura.sq_candidato"))
    ds_url = Column(String)
    cd_tipo_rede_social = Column(String)
