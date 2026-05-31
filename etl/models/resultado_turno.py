from sqlalchemy import Column, BigInteger, Integer, String, ForeignKey, ForeignKeyConstraint, PrimaryKeyConstraint
from .base import Base

class ResultadoTurno(Base):
    __tablename__ = "resultado_turno"

    sq_candidato = Column(BigInteger, ForeignKey("candidatura.sq_candidato"), nullable=False)
    cd_eleicao = Column(BigInteger, nullable=False)
    nr_turno = Column(Integer, nullable=False)
    nr_votos = Column(Integer, default=0)
    cd_sit_tot_turno = Column(Integer)
    ds_sit_tot_turno = Column(String)

    __table_args__ = (
        PrimaryKeyConstraint("sq_candidato", "nr_turno"),
        ForeignKeyConstraint(
            ["cd_eleicao", "nr_turno"],
            ["eleicao.cd_eleicao", "eleicao.nr_turno"]
        ),
    )
