import pytest
from src.models.estrategia import EstrategiaCreate
from src.services.estrategia_service import EstrategiaService
from src.repositories.estrategia_repository import EstrategiaRepository

def test_criar_estrategia(db_session):
    # Testa a criação de uma estratégia
    estrategia = EstrategiaCreate(nome="Tendência de Alta", descricao="Compra em tendência de alta")
    nova_estrategia = EstrategiaService.criar_estrategia(db_session, estrategia.nome, estrategia.descricao)
    assert nova_estrategia.nome == "Tendência de Alta"
    assert nova_estrategia.descricao == "Compra em tendência de alta"

def test_buscar_estrategia_por_id(db_session):
    # Testa a busca de uma estratégia por ID
    estrategia = EstrategiaCreate(nome="Tendência de Alta", descricao="Compra em tendência de alta")
    nova_estrategia = EstrategiaService.criar_estrategia(db_session, estrategia.nome, estrategia.descricao)
    estrategia_buscada = EstrategiaService.buscar_estrategia_por_id(db_session, nova_estrategia.id)
    assert estrategia_buscada.id == nova_estrategia.id