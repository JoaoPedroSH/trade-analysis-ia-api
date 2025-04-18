import os
from fastapi import FastAPI
from src.controllers.usuario_controller import router as usuario_router
from src.controllers.analisador_controller import router as analisador_router
from src.controllers.gestao_risco_controller import router as gestao_risco_router
from src.controllers.estrategia_controller import router as estrategia_router
from src.utils.database import Base, engine
from src.utils.seed import exec_seed

Base.metadata.create_all(bind=engine)

if os.getenv("ENVIRONMENT") == "development":
    exec_seed()

app = FastAPI(
    title="Sistema de Análise de Mercado Financeiro",
    description="API para análise de ativos financeiros com IA.",
    version="0.0.1"
)

app.include_router(usuario_router, prefix="/usuarios", tags=["Usuários"])
app.include_router(analisador_router, prefix="/analisadores", tags=["Analisadores"])
app.include_router(gestao_risco_router, prefix="/gestao-risco", tags=["Gestão de Risco"])
app.include_router(estrategia_router, prefix="/estrategias", tags=["Estratégias"])