from sqlalchemy.orm import Session
from src.models.analisador import Analisador
from src.utils.database import SessionLocal

class AnalisadorRepository:
    @staticmethod
    def criar_analisador(db: Session, simbolo: str, timeframe: str, valor_banca: float, risco_por_operacao: float, data_final: str, usuario_id: int):
        analisador = Analisador(
            simbolo=simbolo,
            timeframe=timeframe,
            valor_banca=valor_banca,
            risco_por_operacao=risco_por_operacao,
            data_final=data_final,
            usuario_id=usuario_id
        )
        db.add(analisador)
        db.commit()
        db.refresh(analisador)
        return analisador

    @staticmethod
    def buscar_analisador_por_id(db: Session, id: int):
        return db.query(Analisador).filter(Analisador.id == id).first()