from sqlalchemy.orm import Session
from src.repositories.gestao_risco_repository import GestaoRiscoRepository

class GestaoRiscoService:
    @staticmethod
    def criar_gestao_risco(db: Session, nome: str, descricao: str):
        return GestaoRiscoRepository.criar_gestao_risco(db, nome, descricao)

    @staticmethod
    def consultar_gestao_risco(db: Session, id: int):
        return GestaoRiscoRepository.buscar_gestao_risco_por_id(db, id)