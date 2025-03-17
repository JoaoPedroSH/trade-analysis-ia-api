from sqlalchemy.orm import Session
from src.repositories.estrategia_repository import EstrategiaRepository

class EstrategiaService:

    @staticmethod
    def criar_estrategia(db: Session, nome: str, descricao: str):
        return EstrategiaRepository.criar_estrategia(db, nome, descricao)

    @staticmethod
    def buscar_estrategia_por_id(db: Session, id: int):
        return EstrategiaRepository.buscar_estrategia_por_id(db, id)

    @staticmethod
    def atualizar_estrategia(db: Session, id: int, nome: str, descricao: str):
        return EstrategiaRepository.atualizar_estrategia(db, id, nome, descricao)

    @staticmethod
    def excluir_estrategia(db: Session, id: int):
        return EstrategiaRepository.excluir_estrategia(db, id)