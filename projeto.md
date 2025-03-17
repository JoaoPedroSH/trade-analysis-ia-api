
---

### *Estrutura do Projeto*

    trade-analysis-ia-api/
    │
    ├── docker-compose.yml        # Configuração do Docker Compose
    ├── README.md                # Configuração do Docker
    ├── .env.example                      # Variáveis de ambiente
    ├── requirements.txt          # Dependências do projeto
    ├── src/                      # Código-fonte do projeto
    │   ├── __init__.py
    |   ├── main.py
    │   ├── models/               # Modelos de dados (ORM)
    │   │   ├── __init__.py
    │   │   ├── usuario.py
    │   │   ├── analise.py
    │   │   ├── gestao_risco.py
    │   │   ├── estrategia.py
    │   │
    │   ├── services/             # Lógica de negócio
    │   │   ├── __init__.py
    │   │   ├── usuario_service.py
    │   │   ├── analise_service.py
    │   │   ├── gestao_risco_service.py
    │   │   ├── estrategia_service.py
    │   │
    │   ├── repositories/         # Acesso ao banco de dados (ORM)
    │   │   ├── __init__.py
    │   │   ├── usuario_repository.py
    │   │   ├── analise_repository.py
    │   │   ├── gestao_risco_repository.py
    │   │   ├── estrategia_repository.py
    │   │
    │   ├── controllers/          # Endpoints da API
    │   │   ├── __init__.py
    │   │   ├── usuario_controller.py
    │   │   ├── analise_controller.py
    │   │   ├── gestao_risco_controller.py
    │   │   ├── estrategia_controller.py
    │   │
    │   ├── utils/                # Utilitários
    │   │   ├── __init__.py
    │   │   ├── auth.py
    │   │   ├── logs.py
    │   │   ├── database.py       # Configuração do banco de dados (ORM)
    │
    ├── tests/                    # Testes automatizados
    │   ├── __init__.py
    |   ├── unit/  
    |   │   ├── conftest.py           # Configurações globais para os testes
    |   │   ├── test_usuario.py       # Testes para o módulo de usuários
    |   │   ├── test_analise.py       # Testes para o módulo de análises
    |   │   ├── test_gestao_risco.py  # Testes para o módulo de gestão de risco
    |   │   ├── test_estrategia.py    # Testes para o módulo de estratégias

---
