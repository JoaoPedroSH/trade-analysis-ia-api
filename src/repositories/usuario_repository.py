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
    def criar_usuario(db: Session, username: str, password_hash: str):
        usuario = Usuario(username=username, password_hash=password_hash)
        db.add(usuario)
        db.commit()
        db.refresh(usuario)
        return usuario

    @staticmethod
    def buscar_usuario_por_username(db: Session, username: str):
        return db.query(Usuario).filter(Usuario.username == username).first()