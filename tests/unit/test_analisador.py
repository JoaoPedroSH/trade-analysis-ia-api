import pytest
from src.models.analisador import AnalisadorRequest
from src.services.analisador_service import AnalisadorService
from src.repositories.analisador_repository import AnalisadorRepository

def test_criar_analisador(db_session):
    # Testa a criação de uma análise
    analisador = AnalisadorRequest(
        simbolo="PETR4",
        timeframe="M1",
        valor_banca=10000.0,
        risco_por_operacao=1.0,
        data_final="2024-01-20"
    )
    nova_analisador = AnalisadorService.criar_analisador(
        db_session,
        analisador.simbolo,
        analisador.timeframe,
        analisador.valor_banca,
        analisador.risco_por_operacao,
        analisador.data_final,
        usuario_id=1
    )
    assert nova_analisador.simbolo == "PETR4"
    assert nova_analisador.timeframe == "M1"
    assert nova_analisador.valor_banca == 10000.0

def test_buscar_analisador_por_id(db_session):
    # Testa a busca de uma análise por ID
    analisador = AnalisadorRequest(
        simbolo="PETR4",
        timeframe="M1",
        valor_banca=10000.0,
        risco_por_operacao=1.0,
        data_final="2024-01-20"
    )
    nova_analisador = AnalisadorRepository.criar_analisador(
        db_session,
        analisador.simbolo,
        analisador.timeframe,
        analisador.valor_banca,
        analisador.risco_por_operacao,
        analisador.data_final,
        usuario_id=1
    )
    analisador_buscada = AnalisadorRepository.buscar_analisador_por_id(db_session, nova_analisador.id)
    assert analisador_buscada.id == nova_analisador.id