from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from pydantic import BaseModel
from src.utils.database import Base

class Analisador(Base):
    __tablename__ = "analisadores"

    id = Column(Integer, primary_key=True, index=True)
    simbolo = Column(String(10), nullable=False)
    timeframe = Column(String(3), nullable=False)
    valor_banca = Column(Float, nullable=False)
    risco_por_operacao = Column(Float, nullable=False)
    data_final = Column(DateTime, nullable=False)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))


class AnalisadorRequest(BaseModel):
    simbolo: str
    timeframe: str
    valor_banca: float
    risco_por_operacao: float
    data_final: str
    usuario_id: int