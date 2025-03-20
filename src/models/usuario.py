from sqlalchemy import Column, Integer, String, Boolean
from pydantic import BaseModel
from src.models.base import Situacao
from src.utils.database import Base

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(50), unique=True, index=True)
    senha_hash = Column(String(255))
    email = Column(String(50), unique=True, index=True)
    email_confirmado = Column(Boolean, default=False)
    situacao = Column(Integer, nullable=False, default=Situacao.ATIVO)
    token_plugin = Column(String(255), nullable=True)
    token_vinculado = Column(Boolean, default=False)

class UsuarioCriar(BaseModel):
    nome: str
    senha: str

class UsuarioRetornoToken(BaseModel):
    access_token: str
    token_type: str