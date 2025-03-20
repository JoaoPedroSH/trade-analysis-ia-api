from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.models.estrategia import EstrategiaCriar, EstrategiaAtualizar
from src.services.estrategia_service import EstrategiaService
from src.utils.auth import obter_usuario_atual
from src.utils.database import get_db

router = APIRouter()

"""
Rotas Públicas
"""
@router.get("/timeframes", summary="Consultar todas os timeframes disponiveis para as estratégias")
async def consultar_timeframes(db: Session = Depends(get_db)):
    timeframes = EstrategiaService.consultar_timeframes(db)
    if not timeframes:
        raise HTTPException(status_code=404, detail="Timeframes não encontrados")
    return timeframes

"""
Rotas Privadas
"""
@router.get("/", summary="Consultar todas as estratégias")
async def buscar_estrategia(id: int, usuario: dict = Depends(obter_usuario_atual), db: Session = Depends(get_db)):
    estrategia = EstrategiaService.buscar_estrategia_por_id(db, id)
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

@router.get("/{id}", summary="Buscar uma estratégia por ID")
async def buscar_estrategia(id: int, usuario: dict = Depends(obter_usuario_atual), db: Session = Depends(get_db)):
    estrategia = EstrategiaService.buscar_estrategia_por_id(db, id)
    if not estrategia:
        raise HTTPException(status_code=404, detail="Estratégia não encontrada")
    return estrategia

@router.put("/{id}", summary="Atualizar uma estratégia")
async def atualizar_estrategia(id: int, estrategia: EstrategiaAtualizar, usuario: dict = Depends(obter_usuario_atual), db: Session = Depends(get_db)):
    try:
        EstrategiaService.atualizar_estrategia(db, id, estrategia.nome, estrategia.descricao)
        return {"mensagem": "Estratégia atualizada com sucesso!"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{id}", summary="Excluir uma estratégia")
async def excluir_estrategia(id: int, usuario: dict = Depends(obter_usuario_atual), db: Session = Depends(get_db)):
    try:
        EstrategiaService.excluir_estrategia(db, id)
        return {"mensagem": "Estratégia excluída com sucesso!"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))