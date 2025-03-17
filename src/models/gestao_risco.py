from pydantic import BaseModel
from sqlalchemy import Column, Integer, String
from src.utils.database import Base

class GestaoRisco(Base):
    __tablename__ = "gestao_risco"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(50), nullable=False)
    descricao = Column(String(255))


class GestaoRiscoCreate(BaseModel):
    nome: str
    descricao: str

class GestaoRiscoUpdate(BaseModel):
    id: int
    nome: str
    descricao: str