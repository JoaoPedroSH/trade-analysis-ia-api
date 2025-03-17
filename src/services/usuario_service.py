from src.repositories.usuario_repository import UsuarioRepository
from src.utils.auth import verificar_senha, gerar_hash_senha

class UsuarioService:
    @staticmethod
    def cadastrar_usuario(db, nome: str, senha: str):
        if UsuarioRepository.buscar_usuario_por_nome(db, nome):
            raise ValueError("Usuário já existe")
        senha_hash = gerar_hash_senha(senha)
        return UsuarioRepository.criar_usuario(db, nome, senha_hash)

    @staticmethod
    def autenticar_usuario(db, nome: str, senha: str):
        usuario = UsuarioRepository.buscar_usuario_por_nome(db, nome)
        if not usuario or not verificar_senha(senha, usuario.senha_hash):
            raise ValueError("Usuário ou senha incorretos")
        return usuario