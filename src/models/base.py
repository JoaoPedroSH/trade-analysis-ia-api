from sqlalchemy import Enum

class Situacao(Enum):
    INATIVO = 0
    ATIVO = 1
    PENDENTE = 2
    CANCELADO = 3
    CONFIRMADO = 4
    FINALIZADO = 5
    