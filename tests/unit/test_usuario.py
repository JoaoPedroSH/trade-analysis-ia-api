import pytest
from src.models.usuario import UsuarioCreate
from src.services.usuario_service import UsuarioService
from src.repositories.usuario_repository import UsuarioRepository

def test_criar_usuario(db_session):
    # Testa a criação de um usuário
    usuario = UsuarioCreate(username="testuser", password="testpassword")
    novo_usuario = UsuarioService.cadastrar_usuario(db_session, usuario.username, usuario.password)
    assert novo_usuario.username == "testuser"
    assert novo_usuario.password_hash is not None

def test_autenticar_usuario(db_session):
    # Testa a autenticação de um usuário
    usuario = UsuarioCreate(username="testuser", password="testpassword")
    UsuarioService.cadastrar_usuario(db_session, usuario.username, usuario.password)
    autenticado = UsuarioService.autenticar_usuario(db_session, "testuser", "testpassword")
    assert autenticado.username == "testuser"

def test_autenticar_usuario_senha_incorreta(db_session):
    # Testa a autenticação com senha incorreta
    usuario = UsuarioCreate(username="testuser", password="testpassword")
    UsuarioService.cadastrar_usuario(db_session, usuario.username, usuario.password)
    with pytest.raises(ValueError):
        UsuarioService.autenticar_usuario(db_session, "testuser", "senha_errada")