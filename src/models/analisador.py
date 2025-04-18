from sqlalchemy import Boolean, Column, Integer, String, DateTime, ForeignKey
from pydantic import BaseModel
from src.utils.database import Base

class Analisador(Base):
    __tablename__ = "analisadores"

    id = Column(Integer, primary_key=True, index=True)
    ativo_financeiro = Column(String(10), nullable=False)
    estrategia_id = Column(Integer, ForeignKey("estrategias.id"))
    gestao_risco_id = Column(Integer, ForeignKey("gestao_riscos.id"))
    situacao = Column(Integer, ForeignKey("analisadores_situacoes.id"))
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    data_criacao = Column(DateTime, nullable=False)
    exclusao_logica = Column(Boolean(False))
    
class AnalisadorSituacao(Base):
    __tablename__ = "analisadores_situacoes"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(10), nullable=False)
    descricao = Column(Integer, ForeignKey("estrategias.id"))
    icone = Column(String(50), nullable=False)
    cor = Column(String(7), nullable=False)

class AnalisadorExecutar(BaseModel):
    ativo_financeiro: str
    timeframe: str
    periodo_analise_dados: int
    saldo: str
    risco: str
    stop_loss_automatico: bool = False
    price_action: str = None
    indicadores: str = None
    dados_historicos: str = None
    dados_indicadores: str = None
    dados_price_action: str = None
    
class AnalisadorSituacaoConsultar(BaseModel):
    id: int
    nome: str
    descricao: str
    icone: str
    cor: str