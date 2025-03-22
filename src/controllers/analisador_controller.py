from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.models.analisador import AnalisadorExecutar
from src.services.analisador_service import AnalisadorService
from src.utils.auth import obter_usuario_atual
from src.utils.database import get_db
import MetaTrader5 as mt5

router = APIRouter()

@router.post("/iniciar/", summary="Iniciar uma nova análise")
async def iniciar_analisador(analise: AnalisadorExecutar, usuario: dict = Depends(obter_usuario_atual), db: Session = Depends(get_db)):
    try:
        # Lógica para iniciar análise
        ...
        return {"id_analise": 1, "mensagem": "Análise iniciada com sucesso!"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))