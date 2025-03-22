from sqlalchemy.orm import Session
from src.models.estrategia import Estrategia, EstrategiaAtivo, EstrategiaIndicador, EstrategiaTimeframe

class EstrategiaRepository:
    @staticmethod
    def criar_estrategia(db: Session ,nome: str, descricao: str):
        estrategia = Estrategia(nome=nome, descricao=descricao)
        db.add(estrategia)
        db.commit()
        db.refresh(estrategia)
        return estrategia

    @staticmethod
    def consultar_estrategia(db: Session, id: int):
        return db.query(Estrategia).filter(Estrategia.id == id).first()
    
    @staticmethod
    def listar_estrategias(db: Session):
        return db.query(Estrategia).all()
    
    @staticmethod
    def listar_timeframes(db: Session):
        return db.query(EstrategiaTimeframe).all()
    
    @staticmethod
    def listar_indicadores(db: Session):
        return db.query(EstrategiaIndicador).all()
    
    @staticmethod
    def listar_ativos(db: Session):
        return db.query(EstrategiaAtivo).all()