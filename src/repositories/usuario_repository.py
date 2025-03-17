from sqlalchemy.orm import Session
from src.models.usuario import Usuario
from src.utils.database import SessionLocal

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class UsuarioRepository:
    @staticmethod
    def criar_usuario(db: Session, nome: str, senha_hash: str):
        usuario = Usuario(nome=nome, senha_hash=senha_hash)
        db.add(usuario)
        db.commit()
        db.refresh(usuario)
        return usuario

    @staticmethod
    def buscar_usuario_por_nome(db: Session, nome: str):
        return db.query(Usuario).filter(Usuario.nome == nome).first()