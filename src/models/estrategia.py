from pydantic import BaseModel
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Boolean
from src.utils.database import Base
    
class Estrategia(Base):
    __tablename__ = "estrategias"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(50), nullable=False)
    descricao = Column(String(255))
    situacao = Column(Integer, ForeignKey("estrategias_situacoes.id"))
    data_criacao = Column(DateTime, nullable=False)
    indicador_id = Column(Integer, ForeignKey("estrategias_indicadores.id"))
    padrao_id = Column(Integer, ForeignKey("estrategias_padroes.id"))
    timeframe_id = Column(Integer, ForeignKey("estrategias_timeframes.id"))
    exclusao_logica = Column(Boolean(False))
    
class EstrategiaSituacao(Base):
    __tablename__ = "estrategias_situacoes"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(50), nullable=False)
    descricao = Column(String(255))
    
class EstrategiaIndicador(Base):
    __tablename__ = "estrategias_indicadores"

    id = Column(Integer, primary_key=True, index=True)
    sigla = Column(String(50), nullable=False)
    descricao = Column(String(255))
    metrica = Column(String(255), nullable=True)
    
class EstrategiaPadrao(Base):
    __tablename__ = "estrategias_padroes"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(50), nullable=False)
    descricao = Column(String(255))
    
class EstrategiaTimeframe(Base):
    __tablename__ = "estrategias_timeframes"

    id = Column(Integer, primary_key=True, index=True)
    sigla = Column(String(50), nullable=False)
    descricao = Column(String(255))
    
class EstrategiaAtivo(Base):
    __tablename__ = "estrategias_ativos"

    id = Column(Integer, primary_key=True, index=True)
    sigla = Column(String(50), nullable=False)
    descricao = Column(String(255))
    
class EstrategiaCriar(BaseModel):
    nome: str
    descricao: str
    situacao_id: int
    indicador_id: int
    padrao_id: int
    timeframe_id: int
 
class EstrategiaSituacaoConsultar(BaseModel):
    id: int
    sigla: str
    descricao: str
    
class EstrategiaIndicadorConsultar(BaseModel):
    id: int
    sigla: str
    descricao: str
    
class EstrategiaAtivoConsultar(BaseModel):
    id: int
    sigla: str
    descricao: str
    
class EstrategiaPadraoConsultar(BaseModel):
    id: int
    sigla: str
    descricao: str
      
class EstrategiaTimeframeConsultar(BaseModel):
    id: int
    sigla: str
    descricao: str
    
