from sqlalchemy.orm import Session
from src.models.gestao_risco import GestaoRisco
from src.utils.database import SessionLocal

class GestaoRiscoRepository:
    @staticmethod
    def criar_gestao_risco(db: Session, nome: str, descricao: str):
        gestao_risco = GestaoRisco(nome=nome, descricao=descricao)
        db.add(gestao_risco)
        db.commit()
        db.refresh(gestao_risco)
        return gestao_risco

    @staticmethod
    def buscar_gestao_risco_por_id(db: Session, id: int):
        return db.query(GestaoRisco).filter(GestaoRisco.id == id).first()