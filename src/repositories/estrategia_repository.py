from sqlalchemy.orm import Session
from src.models.estrategia import Estrategia, EstrategiaTimeframe
from src.utils.database import SessionLocal

class EstrategiaRepository:
    @staticmethod
    def criar_estrategia(db: Session, nome: str, descricao: str):
        estrategia = Estrategia(nome=nome, descricao=descricao)
        db.add(estrategia)
        db.commit()
        db.refresh(estrategia)
        return estrategia

    @staticmethod
    def buscar_estrategia_por_id(db: Session, id: int):
        return db.query(Estrategia).filter(Estrategia.id == id).first()
    
    @staticmethod
    def consultar_timeframes(db: Session):
        return db.query(EstrategiaTimeframe).all()