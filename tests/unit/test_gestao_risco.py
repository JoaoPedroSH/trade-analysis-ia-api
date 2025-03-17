import pytest
from src.models.gestao_risco import GestaoRiscoCreate
from src.services.gestao_risco_service import GestaoRiscoService
from src.repositories.gestao_risco_repository import GestaoRiscoRepository

def test_criar_gestao_risco(db_session):
    # Testa a criação de uma gestão de risco
    gestao_risco = GestaoRiscoCreate(nome="Risco Baixo", descricao="Risco de até 1%")
    nova_gestao_risco = GestaoRiscoService.criar_gestao_risco(db_session, gestao_risco.nome, gestao_risco.descricao)
    assert nova_gestao_risco.nome == "Risco Baixo"
    assert nova_gestao_risco.descricao == "Risco de até 1%"

def test_buscar_gestao_risco_por_id(db_session):
    # Testa a busca de uma gestão de risco por ID
    gestao_risco = GestaoRiscoCreate(nome="Risco Baixo", descricao="Risco de até 1%")
    nova_gestao_risco = GestaoRiscoService.criar_gestao_risco(db_session, gestao_risco.nome, gestao_risco.descricao)
    gestao_risco_buscada = GestaoRiscoService.buscar_gestao_risco_por_id(db_session, nova_gestao_risco.id)
    assert gestao_risco_buscada.id == nova_gestao_risco.id