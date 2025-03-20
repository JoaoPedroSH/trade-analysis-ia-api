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

@router.get("/timeframes/", summary="Listar timeframes disponíveis")
async def listar_timeframes(usuario: dict = Depends(obter_usuario_atual)):
    # Timeframes disponíveis no MT5
    timeframes = {
        "M1": mt5.TIMEFRAME_M1,
        "M5": mt5.TIMEFRAME_M5,
        "M15": mt5.TIMEFRAME_M15,
        "H1": mt5.TIMEFRAME_H1,
        "H4": mt5.TIMEFRAME_H4,
        "D1": mt5.TIMEFRAME_D1,
        "W1": mt5.TIMEFRAME_W1,
        "MN1": mt5.TIMEFRAME_MN1
    }
    return timeframes

@router.get("/indicadores/", summary="Listar indicadores disponíveis")
async def listar_indicadores(usuario: dict = Depends(obter_usuario_atual)):
    # Lista de indicadores suportados (pode ser expandida)
    indicadores = [
        "SMA", "EMA", "RSI", "MACD", "Bollinger Bands",
        "Stochastic", "ATR", "ADX", "CCI", "Fibonacci"
    ]
    return indicadores

@router.get("/ativos/", summary="Listar ativos disponíveis")
async def listar_ativos():

    ativos = mt5.symbols_total()
    return ativos