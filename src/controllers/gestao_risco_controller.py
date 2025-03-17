from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.models.gestao_risco import GestaoRiscoCreate, GestaoRiscoUpdate
from src.services.gestao_risco_service import GestaoRiscoService
from src.utils.auth import obter_usuario_atual
from src.utils.database import get_db

router = APIRouter()

@router.post("/", summary="Criar uma nova gestão de risco")
async def criar_gestao_risco(gestao_risco: GestaoRiscoCreate, usuario: dict = Depends(obter_usuario_atual), db: Session = Depends(get_db)):
    try:
        GestaoRiscoService.criar_gestao_risco(db, gestao_risco.nome, gestao_risco.descricao)
        return {"mensagem": "Gestão de risco criada com sucesso!"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{id}", summary="Buscar uma gestão de risco por ID")
async def buscar_gestao_risco(id: int, usuario: dict = Depends(obter_usuario_atual), db: Session = Depends(get_db)):
    gestao_risco = GestaoRiscoService.buscar_gestao_risco_por_id(db, id)
    if not gestao_risco:
        raise HTTPException(status_code=404, detail="Gestão de risco não encontrada")
    return gestao_risco

@router.put("/{id}", summary="Atualizar uma gestão de risco")
async def atualizar_gestao_risco(id: int, gestao_risco: GestaoRiscoUpdate, usuario: dict = Depends(obter_usuario_atual), db: Session = Depends(get_db)):
    try:
        GestaoRiscoService.atualizar_gestao_risco(db, id, gestao_risco.nome, gestao_risco.descricao)
        return {"mensagem": "Gestão de risco atualizada com sucesso!"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{id}", summary="Excluir uma gestão de risco")
async def excluir_gestao_risco(id: int, usuario: dict = Depends(obter_usuario_atual), db: Session = Depends(get_db)):
    try:
        GestaoRiscoService.excluir_gestao_risco(db, id)
        return {"mensagem": "Gestão de risco excluída com sucesso!"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))