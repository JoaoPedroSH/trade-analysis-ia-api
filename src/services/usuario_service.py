from src.repositories.usuario_repository import UsuarioRepository
from src.utils.auth import verificar_senha, gerar_hash_senha

class UsuarioService:
    @staticmethod
    def cadastrar_usuario(db, username: str, password: str):
        if UsuarioRepository.buscar_usuario_por_username(db, username):
            raise ValueError("Usuário já existe")
        password_hash = gerar_hash_senha(password)
        return UsuarioRepository.criar_usuario(db, username, password_hash)

    @staticmethod
    def autenticar_usuario(db, username: str, password: str):
        usuario = UsuarioRepository.buscar_usuario_por_username(db, username)
        if not usuario or not verificar_senha(password, usuario.password_hash):
            raise ValueError("Usuário ou senha incorretos")
        return usuario