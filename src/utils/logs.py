from src.utils.database import get_db
from sqlalchemy.orm import Session

def registrar_log(usuario_id: int, acao: str, db: Session = next(get_db())):
    # Exemplo de função para registrar logs no banco de dados
    # Você pode expandir isso para incluir mais detalhes ou usar um sistema de logs externo
    from src.models.log import Log  # Supondo que você tenha um modelo de Log
    log = Log(usuario_id=usuario_id, acao=acao)
    db.add(log)
    db.commit()
    db.refresh(log)
    return log

