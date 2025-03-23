from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.models.analisador import AnalisadorExecutar
from src.services.analisador_service import AnalisadorService
from src.utils.auth import obter_usuario_atual
from src.utils.database import get_db
from src.utils.ia import pipe
import threading
import time

router = APIRouter()

# Dicionário para armazenar o estado das análises em execução
analises_em_execucao = {}

@router.post("/iniciar", summary="Iniciar uma nova análise")
async def iniciar_analisador(analise: AnalisadorExecutar, usuario: dict = Depends(obter_usuario_atual), db: Session = Depends(get_db)):
    try:
        # Verifica se a análise já está em execução
        if analise.ativo_financeiro in analises_em_execucao and analises_em_execucao[analise.ativo_financeiro]["executando"]:
            raise HTTPException(status_code=400, detail="Análise já está em execução para este ativo.")

        # Define o estado inicial da análise
        analises_em_execucao[analise.ativo_financeiro] = {
            "executando": True,
            "thread": threading.Thread(target=AnalisadorService.executar_analise, args=(analise, db))
        }

        # Inicia a thread para executar a análise
        analises_em_execucao[analise.ativo_financeiro]["thread"].start()

        return {"mensagem": f"Análise para o ativo {analise.ativo_financeiro} iniciada com sucesso!"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/parar", summary="Parar uma análise em execução")
async def parar_analisador(ativo_financeiro: str, usuario: dict = Depends(obter_usuario_atual)):
    try:
        # Verifica se a análise está em execução
        if ativo_financeiro not in analises_em_execucao or not analises_em_execucao[ativo_financeiro]["executando"]:
            raise HTTPException(status_code=400, detail="Nenhuma análise em execução para este ativo.")

        # Atualiza o estado para parar a análise
        analises_em_execucao[ativo_financeiro]["executando"] = False

        return {"mensagem": f"Análise para o ativo {ativo_financeiro} parada com sucesso!"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/executar", summary="Executar uma análise manualmente")
async def iniciar_analisador(analise: AnalisadorExecutar, usuario: dict = Depends(obter_usuario_atual), db: Session = Depends(get_db)):
    try:
        return AnalisadorService.executar_analise(analise, db)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))