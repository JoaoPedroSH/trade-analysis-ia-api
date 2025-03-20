from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from pydantic import BaseModel
from src.models.base import Situacao
from src.utils.database import Base

class Analisador(Base):
    __tablename__ = "analisadores"

    id = Column(Integer, primary_key=True, index=True)
    ativo_financeiro = Column(String(10), nullable=False)
    estrategia_id = Column(Integer, ForeignKey("estrategias.id"))
    gestao_risco_id = Column(Integer, ForeignKey("gestao_riscos.id"))
    situacao = Column(Integer, nullable=False, default=Situacao.INATIVO)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    data_criacao = Column(DateTime, nullable=False)

class AnalisadorExecutar(BaseModel):
    ativo_financeiro: str
    timeframe: str
    indicador: str
    padrao: str
    tipo_gestao: str
    valor_banca: float
    risco_por_operacao: float
    stop_ganho: float
    stop_perda: float
    valor_entrada: float
    token: str
    usuario_id: int