from src.models.estrategia import EstrategiaTimeframe
from src.models.usuario import Usuario
from src.utils.database import get_db
from src.utils.auth import gerar_hash_senha
import os
    
def add_if_not_exists(session, model, **kwargs):
    instance = session.query(model).filter_by(**kwargs).first()
    if not instance:
        instance = model(**kwargs)
        session.add(instance)
        session.commit()
    return instance

def exec_seed():
    db = next(get_db())
    try:
        print("Executando seed...")
        print("Populando a tabela de Timeframes")
        add_if_not_exists(db, EstrategiaTimeframe, sigla="M5", descricao="5 Minutos", situacao=1)
        add_if_not_exists(db, EstrategiaTimeframe, sigla="M10", descricao="10 Minutos", situacao=1)
        add_if_not_exists(db, EstrategiaTimeframe, sigla="M15", descricao="15 Minutos", situacao=1)
        add_if_not_exists(db, EstrategiaTimeframe, sigla="M20", descricao="20 Minutos", situacao=1)
        add_if_not_exists(db, EstrategiaTimeframe, sigla="M30", descricao="30 Minutos", situacao=1)
        
        print("Criando usuário padrão")
        add_if_not_exists(db, Usuario, nome=os.getenv("NOME_USUARIO_PADRAO"), senha_hash=gerar_hash_senha(os.getenv("SENHA_USUARIO_PADRAO")), situacao=1)
        
        print("Seed executado com sucesso!")
    except Exception as e:
        print(f"Erro ao executar seed: {e}")
        db.rollback()