import json
from fastapi import APIRouter, Depends, HTTPException, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session
from src.models.analisador import AnalisadorExecutar
from src.services.analisador_service import AnalisadorService
from src.utils.auth import obter_usuario_atual
from src.utils.database import get_db

router = APIRouter()

conexoes_ws_ativas = {}


@router.post("/iniciar", summary="Iniciar uma nova análise")
async def iniciar_analisador(
    analise: AnalisadorExecutar,
    usuario: dict = Depends(obter_usuario_atual),
    db: Session = Depends(get_db),
):
    try:
        # Verifica se a análise já está em execução
        if analise.ativo_financeiro in conexoes_ws_ativas:
            raise HTTPException(status_code=400, detail="Análise já está em execução para este ativo.")

        # Serializa os dados da análise
        analise_data = {
            "ativo_financeiro": analise.ativo_financeiro,
            "timeframe": analise.timeframe,
        }

        # Inicia a tarefa Celery
        tarefa = AnalisadorService.executar_analise.apply_async(args=[analise_data, None])

        # Armazena a tarefa no dicionário de conexões
        conexoes_ws_ativas[analise.ativo_financeiro] = tarefa

        return {"mensagem": f"Análise para o ativo {analise.ativo_financeiro} iniciada com sucesso!", "tarefa_id": tarefa.id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.websocket("/ws/{ativo_financeiro}")
async def websocket_endpoint(websocket: WebSocket, ativo_financeiro: str):
    await websocket.accept()

    try:
        while True:
            # Verifica o estado da tarefa
            if ativo_financeiro in conexoes_ws_ativas:
                tarefa = conexoes_ws_ativas[ativo_financeiro]
                estado = tarefa.state
                meta = tarefa.info

                # Envia atualizações de progresso
                if estado == "PROGRESS":
                    await websocket.send_text(json.dumps({"progresso": meta["progresso"]}))
                elif estado == "SUCCESS":
                    await websocket.send_text(json.dumps({"status": "concluido"}))
                    break
                elif estado == "FAILURE":
                    await websocket.send_text(json.dumps({"status": "erro", "erro": str(tarefa.info)}))
                    break

            await websocket.receive_text()  # Mantém a conexão aberta
    except WebSocketDisconnect:
        del conexoes_ws_ativas[ativo_financeiro]