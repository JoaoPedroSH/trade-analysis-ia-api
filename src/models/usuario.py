from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from pydantic import BaseModel
from src.utils.database import Base

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(50), unique=True, index=True)
    senha_hash = Column(String(255))
    email = Column(String(50), unique=True, index=True)
    email_confirmado = Column(Boolean, default=False)
    situacao_id = Column(Integer, ForeignKey("usuarios_situacoes.id"))
    token_plugin = Column(String(255), nullable=True)
    token_vinculado = Column(Boolean, default=False)
    
class UsuarioSituacao(Base):
    __tablename__ = "usuarios_situacoes"
    
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(50), nullable=False)
    descricao = Column(String(255))

class UsuarioCriar(BaseModel):
    nome: str
    senha: str

class UsuarioRetornoToken(BaseModel):
    access_token: str
    token_type: str
    
class UsuarioSitacaoConsultar(BaseModel):
    id: int
    nome: str
    descricao: str