from pydantic import BaseModel
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from src.models.base import Situacao
from src.utils.database import Base
    
class Estrategia(Base):
    __tablename__ = "estrategias"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(50), nullable=False)
    descricao = Column(String(255))
    situacao = Column(Integer, nullable=False, default=Situacao.ATIVO)
    data_criacao = Column(DateTime, nullable=False)
    indicador_id = Column(Integer, ForeignKey("estrategias_indicadores.id"))
    padrao_id = Column(Integer, ForeignKey("estrategias_padroes.id"))
    timeframe_id = Column(Integer, ForeignKey("estrategias_timeframes.id"))
    
class EstrategiaIndicador(Base):
    __tablename__ = "estrategias_indicadores"

    id = Column(Integer, primary_key=True, index=True)
    sigla = Column(String(50), nullable=False)
    descricao = Column(String(255))
    situacao = Column(Integer, nullable=False, default=Situacao.ATIVO)
    
class EstrategiaPadrao(Base):
    __tablename__ = "estrategias_padroes"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(50), nullable=False)
    descricao = Column(String(255))
    situacao = Column(Integer, nullable=False, default=Situacao.ATIVO)
    
class EstrategiaTimeframe(Base):
    __tablename__ = "estrategias_timeframes"

    id = Column(Integer, primary_key=True, index=True)
    sigla = Column(String(50), nullable=False)
    descricao = Column(String(255))
    situacao = Column(Integer, nullable=False, default=Situacao.ATIVO)
    
class EstrategiaCriar(BaseModel):
    nome: str
    descricao: str
    situacao: int
    indicador_id: int
    padrao_id: int
    
class EstrategiaAtualizar(BaseModel):
    nome: str
    descricao: str
    situacao: int
    indicador_id: int
    padrao_id: int
 
class EstrategiaIndicadorConsultar(BaseModel):
    id: int
    sigla: str
    descricao: str
    situacao: int
    
class EstrategiaPadraoConsultar(BaseModel):
    id: int
    sigla: str
    descricao: str
    situacao: int
      
class EstrategiaTimeframeConsultar(BaseModel):
    id: int
    sigla: str
    descricao: str
    situacao: int
    
