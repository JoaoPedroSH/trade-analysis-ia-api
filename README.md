# trade-analysis-ia-api

---
### *Estrutura do Projeto*

    trade-analysis-ia-api/
    │
    ├── docker-compose.yml
    ├── README.md
    ├── .env.example
    ├── requirements.txt
    ├── src/
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
    │   │   ├── database.py      
    │
    ├── tests/                    # Testes automatizados
    │   ├── __init__.py
    |   ├── unit/  
    |   │   ├── conftest.py           
    |   │   ├── test_usuario.py      
    |   │   ├── test_analise.py       
    |   │   ├── test_gestao_risco.py  
    |   │   ├── test_estrategia.py    

---


### *Como Executar o Projeto*

*Execute os testes*:
   - No terminal, navegue até a pasta do projeto e execute: ´pytest tests/´.
   
*Inicializar banco de dados*
   - No terminal, navegue até a pasta do projeto e execute ´docker-compose up --build´ para construir e iniciar conteiner msqly.

*Preparar ambiente virtual do python e subir o software*
   - Execute ´python -m venv .venv´ e ´.venv\Scripts\Active´ para gerar e ativar o ambiente
   - ´pip install -r requirements.txt´ para instalar as dependencias
   - Em seguida, execute ´fastapi dev src/main.py --reload´ para rodar a aplicação


### *Links úteis*
- https://www.mql5.com/en/docs/python_metatrader5