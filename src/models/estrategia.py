from pydantic import BaseModel
from sqlalchemy import Column, Integer, String
from src.utils.database import Base

class Estrategia(Base):
    __tablename__ = "estrategias"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(50), nullable=False)
    descricao = Column(String(255))

class EstrategiaCreate(BaseModel):
    nome: str
    descricao: str

class EstrategiaUpdate(BaseModel):
    id: int
    nome: str
    descricao: str