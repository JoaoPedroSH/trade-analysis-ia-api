from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.models.gestao_risco import GestaoRiscoCriar
from src.services.gestao_risco_service import GestaoRiscoService
from src.utils.auth import obter_usuario_atual
from src.utils.database import get_db

router = APIRouter()

@router.post("/", summary="Criar uma nova gestão de risco")
async def criar_gestao_risco(gestao_risco: GestaoRiscoCriar, usuario: dict = Depends(obter_usuario_atual), db: Session = Depends(get_db)):
    try:
        GestaoRiscoService.criar_gestao_risco(db, gestao_risco.nome, gestao_risco.descricao)
        return {"mensagem": "Gestão de risco criada com sucesso!"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{id}", summary="Consultar uma gestão de risco por ID")
async def consultar_gestao_risco(id: int, usuario: dict = Depends(obter_usuario_atual), db: Session = Depends(get_db)):
    gestao_risco = GestaoRiscoService.consultar_gestao_risco(db, id)
    if not gestao_risco:
        raise HTTPException(status_code=404, detail="Gestão de risco não encontrada")
    return gestao_risco