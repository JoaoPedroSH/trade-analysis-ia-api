from pydantic import BaseModel
from sqlalchemy import Column, Float, ForeignKey, Integer, String, Boolean
from src.models.base import Situacao
from src.utils.database import Base

class GestaoRisco(Base):
    __tablename__ = "gestao_riscos"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(50), nullable=False)
    descricao = Column(String(255))
    valor_banca = Column(Float, nullable=False)
    risco_por_operacao = Column(Float, nullable=False)
    tipo_gestao_id = Column(Integer, ForeignKey("gestao_riscos_tipos.id"))
    situacao = Column(Integer, nullable=False, default=Situacao.ATIVO)
    stops_predefinidos = Column(Boolean, default=False)
    stop_ganho = Column(Float, nullable=True)
    stop_perda = Column(Float, nullable=True)
    valor_entrada = Column(Float, nullable=False)
    
class GestaoRiscoTipo(Base):
    __tablename__ = "gestao_riscos_tipos"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(50), nullable=False)
    descricao = Column(String(255))
    situacao = Column(Integer, nullable=False, default=Situacao.ATIVO)

class GestaoRiscoCriar(BaseModel):
    nome: str
    descricao: str
    risco_por_operacao: float
    tipo_gestao: int
    situacao: int
    
class GestaoRiscoAtualizar(BaseModel):
    nome: str
    descricao: str
    risco_por_operacao: float
    tipo_gestao: int
    situacao: int