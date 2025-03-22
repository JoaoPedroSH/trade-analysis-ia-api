from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.models.estrategia import EstrategiaCriar
from src.services.estrategia_service import EstrategiaService
from src.utils.auth import obter_usuario_atual
from src.utils.database import get_db

router = APIRouter()

@router.get("/timeframes", summary="Listar todos os timeframes disponíveis")
async def listar_timeframes(usuario: dict = Depends(obter_usuario_atual), db: Session = Depends(get_db)):
    timeframes = EstrategiaService.listar_timeframes(db)
    if not timeframes:
        raise HTTPException(status_code=404, detail="Timeframes não encontrados")
    return timeframes

@router.get("/indicadores", summary="Listar todos os indicadores disponíveis")
async def listar_indicadores(usuario: dict = Depends(obter_usuario_atual), db: Session = Depends(get_db)):
    indicadores = EstrategiaService.listar_indicadores(db)
    if not indicadores:
        raise HTTPException(status_code=404, detail="Indicadores não encontrados")
    return indicadores

@router.get("/ativos", summary="Listar todos os ativos disponíveis")
async def listar_ativos(usuario: dict = Depends(obter_usuario_atual), db: Session = Depends(get_db)):
    ativos = EstrategiaService.listar_ativos(db)
    if not ativos:
        raise HTTPException(status_code=404, detail="Ativos não encontrados")
    return ativos

@router.get("/", summary="Consultar todas as estratégias")
async def consultar_estrategia(id: int, usuario: dict = Depends(obter_usuario_atual), db: Session = Depends(get_db)):
    estrategia = EstrategiaService.consultar_estrategia(db, id)
    if not estrategia:
        raise HTTPException(status_code=404, detail="Estratégia não encontrada")
    return estrategia

@router.post("/", summary="Criar uma nova estratégia")
async def criar_estrategia(estrategia: EstrategiaCriar, usuario: dict = Depends(obter_usuario_atual), db: Session = Depends(get_db)):
    try:
        EstrategiaService.criar_estrategia(db, estrategia.nome, estrategia.descricao)
        return {"mensagem": "Estratégia criada com sucesso!"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))