from sqlalchemy.orm import Session
from src.repositories.estrategia_repository import EstrategiaRepository

class EstrategiaService:

    @staticmethod
    def criar_estrategia(db: Session, nome: str, descricao: str):
        return EstrategiaRepository.criar_estrategia(db, nome, descricao)

    @staticmethod
    def consultar_estrategia(db: Session, id: int):
        return EstrategiaRepository.consultar_estrategia(db, id)

    @staticmethod
    def listar_estrategias(db: Session):
        return EstrategiaRepository.listar_estrategias(db)
    
    @staticmethod
    def listar_timeframes(db: Session):
        return EstrategiaRepository.listar_timeframes(db)
    
    @staticmethod
    def listar_indicadores(db: Session):
        return EstrategiaRepository.listar_indicadores(db)
    
    @staticmethod
    def listar_ativos(db: Session):
        return EstrategiaRepository.listar_timeframes(db)