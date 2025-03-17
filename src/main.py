from fastapi import FastAPI
# from src.controllers.usuario_controller import router as usuario_router
# from src.controllers.analise_controller import router as analise_router
# from src.controllers.gestao_risco_controller import router as gestao_risco_router
# from src.controllers.estrategia_controller import router as estrategia_router
from src.utils.database import Base, engine

# Cria as tabelas no banco de dados (se não existirem)
Base.metadata.create_all(bind=engine)

# Configuração do FastAPI
app = FastAPI(
    title="Sistema de Análise de Mercado Financeiro",
    description="API para análise de ativos financeiros com IA.",
    version="1.0.0",
    docs_url="/docs",  # Ativa o Swagger UI
    redoc_url="/redoc"  # Ativa o ReDoc
)

# Registrar rotas
# app.include_router(usuario_router, prefix="/usuarios", tags=["Usuários"])
# app.include_router(analise_router, prefix="/analise", tags=["Análise"])
# app.include_router(gestao_risco_router, prefix="/gestao-risco", tags=["Gestão de Risco"])
# app.include_router(estrategia_router, prefix="/estrategias", tags=["Estratégias"])