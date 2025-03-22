from pydantic import BaseModel
from sqlalchemy import Column, Float, ForeignKey, Integer, String, Boolean
from src.utils.database import Base

class GestaoRisco(Base):
    __tablename__ = "gestao_riscos"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(50), nullable=False)
    descricao = Column(String(255))
    valor_banca = Column(Float, nullable=False)
    risco_por_operacao = Column(Float, nullable=False)
    tipo_gestao_id = Column(Integer, ForeignKey("gestao_riscos_tipos.id"))
    situacao_id = Column(Integer, ForeignKey("gestao_riscos_situacoes.id"))
    stops_predefinidos = Column(Boolean(False))
    stop_ganho = Column(Float, nullable=True)
    stop_perda = Column(Float, nullable=True)
    valor_entrada = Column(Float, nullable=False)
    exclusao_logica = Column(Boolean(False))
    
class GestaoRiscoSituacao(Base):
    __tablename__ = "gestao_riscos_situacoes"
    
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(50), nullable=False)
    descricao = Column(String(255))
    
class GestaoRiscoTipo(Base):
    __tablename__ = "gestao_riscos_tipos"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(50), nullable=False)
    descricao = Column(String(255))

class GestaoRiscoCriar(BaseModel):
    nome: str
    descricao: str
    risco_por_operacao: float
    tipo_gestao: int
    situacao: int
    
class GestaoRiscoSituacaoConsultar(BaseModel):
    id: int
    nome: str
    descricao: str