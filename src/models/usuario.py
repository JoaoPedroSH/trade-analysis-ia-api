from sqlalchemy import Column, Integer, String
from pydantic import BaseModel
from src.utils.database import Base

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(50), unique=True, index=True)
    senha_hash = Column(String(255))


class UsuarioCreate(BaseModel):
    nome: str
    senha: str


class UsuarioLogin(BaseModel):
    nome: int
    senha: str