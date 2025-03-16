
---

### *Estrutura do Projeto*

    projeto/
    │
    ├── docker-compose.yml        # Configuração do Docker Compose
    ├── Dockerfile                # Configuração do Docker
    ├── .env                      # Variáveis de ambiente
    ├── requirements.txt          # Dependências do projeto
    ├── src/                      # Código-fonte do projeto
    │   ├── __init__.py
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
    │   ├── conftest.py           # Configurações globais para os testes
    │   ├── test_usuario.py       # Testes para o módulo de usuários
    │   ├── test_analise.py       # Testes para o módulo de análises
    │   ├── test_gestao_risco.py  # Testes para o módulo de gestão de risco
    │   ├── test_estrategia.py    # Testes para o módulo de estratégias



---

### *Conteúdo dos Arquivos*

#### 1. docker-compose.yml
    version: '3.8'
    
    services:
      db:
        image: mysql:8.0
        container_name: mysql_db
        environment:
          MYSQL_ROOT_PASSWORD: ${DB_ROOT_PASSWORD}
          MYSQL_DATABASE: ${DB_NAME}
          MYSQL_USER: ${DB_USER}
          MYSQL_PASSWORD: ${DB_PASSWORD}
        ports:
          - "3306:3306"
        volumes:
          - db_data:/var/lib/mysql
        networks:
          - app_network
    
      app:
        build: .
        container_name: fastapi_app
        ports:
          - "8000:8000"
        environment:
          - DB_HOST=db
          - DB_NAME=${DB_NAME}
          - DB_USER=${DB_USER}
          - DB_PASSWORD=${DB_PASSWORD}
          - SECRET_KEY=${SECRET_KEY}
          - ALGORITHM=${ALGORITHM}
          - ACCESS_TOKEN_EXPIRE_MINUTES=${ACCESS_TOKEN_EXPIRE_MINUTES}
        depends_on:
          - db
        networks:
          - app_network
    
    volumes:
      db_data:
    
    networks:
      app_network:


---

#### 2. Dockerfile
    dockerfile
    FROM python:3.9-slim
    
    WORKDIR /app
    
    COPY requirements.txt .
    RUN pip install --no-cache-dir -r requirements.txt
    
    COPY . .
    
    CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]


---

#### 3. .env
# Configurações do banco de dados
    DB_HOST=db
    DB_NAME=mercado_financeiro
    DB_USER=root
    DB_PASSWORD=senha_segura
    DB_ROOT_PASSWORD=senha_segura

# Configurações do FastAPI
    SECRET_KEY=sua_chave_secreta
    ALGORITHM=HS256
    ACCESS_TOKEN_EXPIRE_MINUTES=30


---

#### 4. requirements.txt
    fastapi
    uvicorn
    mysql-connector-python
    MetaTrader5
    pandas
    pandas_ta
    transformers
    python-jose[cryptography]
    passlib
    bcrypt
    sqlalchemy
    python-dotenv
    pytest


---

#### 5. src/utils/database.py (Configuração do ORM)
    from sqlalchemy import create_engine
    from sqlalchemy.ext.declarative import declarative_base
    from sqlalchemy.orm import sessionmaker
    from dotenv import load_dotenv
    import os
    
    load_dotenv()

# Configuração do banco de dados
    DB_HOST = os.getenv("DB_HOST")
    DB_NAME = os.getenv("DB_NAME")
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    
    DATABASE_URL = f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
    
    engine = create_engine(DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    Base = declarative_base()


---

#### 6. src/models/usuario.py (Modelo de Usuário com ORM)
    from sqlalchemy import Column, Integer, String
    from src.utils.database import Base
    
    class Usuario(Base):
        __tablename__ = "usuarios"
    
        id = Column(Integer, primary_key=True, index=True)
        username = Column(String(50), unique=True, index=True)
        password_hash = Column(String(255))


---

#### 7. src/models/analise.py (Modelo de Análise com ORM)
    from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
    from src.utils.database import Base
    
    class Analise(Base):
        __tablename__ = "analises"
    
        id = Column(Integer, primary_key=True, index=True)
        simbolo = Column(String(10), nullable=False)
        timeframe = Column(String(3), nullable=False)
        valor_banca = Column(Float, nullable=False)
        risco_por_operacao = Column(Float, nullable=False)
        data_final = Column(DateTime, nullable=False)
        usuario_id = Column(Integer, ForeignKey("usuarios.id"))


---

#### 8. src/models/gestao_risco.py (Modelo de Gestão de Risco com ORM)
    from sqlalchemy import Column, Integer, String
    from src.utils.database import Base
    
    class GestaoRisco(Base):
        __tablename__ = "gestao_risco"
    
        id = Column(Integer, primary_key=True, index=True)
        nome = Column(String(50), nullable=False)
        descricao = Column(String(255))


---

#### 9. src/models/estrategia.py (Modelo de Estratégia com ORM)
    from sqlalchemy import Column, Integer, String
    from src.utils.database import Base
    
    class Estrategia(Base):
        __tablename__ = "estrategias"
    
        id = Column(Integer, primary_key=True, index=True)
        nome = Column(String(50), nullable=False)
        descricao = Column(String(255))


---

#### 10. src/repositories/usuario_repository.py (Repositório de Usuários com ORM)
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


---

#### 11. src/repositories/analise_repository.py (Repositório de Análise com ORM)
    from sqlalchemy.orm import Session
    from src.models.analise import Analise
    from src.utils.database import SessionLocal
    
    class AnaliseRepository:
        @staticmethod
        def criar_analise(db: Session, simbolo: str, timeframe: str, valor_banca: float, risco_por_operacao: float, data_final: str, usuario_id: int):
            analise = Analise(
                simbolo=simbolo,
                timeframe=timeframe,
                valor_banca=valor_banca,
                risco_por_operacao=risco_por_operacao,
                data_final=data_final,
                usuario_id=usuario_id
            )
            db.add(analise)
            db.commit()
            db.refresh(analise)
            return analise
    
        @staticmethod
        def buscar_analise_por_id(db: Session, id: int):
            return db.query(Analise).filter(Analise.id == id).first()


---

#### 12. src/repositories/gestao_risco_repository.py (Repositório de Gestão de Risco com ORM)
    from sqlalchemy.orm import Session
    from src.models.gestao_risco import GestaoRisco
    from src.utils.database import SessionLocal
    
    class GestaoRiscoRepository:
        @staticmethod
        def criar_gestao_risco(db: Session, nome: str, descricao: str):
            gestao_risco = GestaoRisco(nome=nome, descricao=descricao)
            db.add(gestao_risco)
            db.commit()
            db.refresh(gestao_risco)
            return gestao_risco
    
        @staticmethod
        def buscar_gestao_risco_por_id(db: Session, id: int):
            return db.query(GestaoRisco).filter(GestaoRisco.id == id).first()


---

#### 13. src/repositories/estrategia_repository.py (Repositório de Estratégia com ORM)
    from sqlalchemy.orm import Session
    from src.models.estrategia import Estrategia
    from src.utils.database import SessionLocal
    
    class EstrategiaRepository:
        @staticmethod
        def criar_estrategia(db: Session, nome: str, descricao: str):
            estrategia = Estrategia(nome=nome, descricao=descricao)
            db.add(estrategia)
            db.commit()
            db.refresh(estrategia)
            return estrategia
    
        @staticmethod
        def buscar_estrategia_por_id(db: Session, id: int):
            return db.query(Estrategia).filter(Estrategia.id == id).first()


---

#### 14. src/services/usuario_service.py (Serviço de Usuários)
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


---

#### 15. src/services/analise_service.py (Serviço de Análise)
    import MetaTrader5 as mt5
    import pandas as pd
    import pandas_ta as ta
    from datetime import datetime
    from src.repositories.analise_repository import AnaliseRepository
    from src.utils.database import get_db
    
    class AnaliseService:
        @staticmethod
        def calcular_gestao_risco(valor_banca: float, risco_por_operacao: float, preco_atual: float):
            risco_maximo = valor_banca * (risco_por_operacao / 100)
            stop_loss = preco_atual * 0.98  # Exemplo: 2% abaixo do preço atual
            stop_gain = preco_atual * 1.02  # Exemplo: 2% acima do preço atual
            tamanho_posicao = risco_maximo / (preco_atual - stop_loss)
            return stop_loss, stop_gain, tamanho_posicao
    
        @staticmethod
        def sugerir_estrategia(dados: pd.DataFrame):
            # Exemplo de lógica para sugerir estratégia
            if dados['close'].iloc[-1] > dados['SMA_20'].iloc[-1]:
                return "Tendência de Alta"
            else:
                return "Tendência de Baixa"
    
        @staticmethod
        def sugerir_gestao_risco(valor_banca: float, risco_por_operacao: float):
            # Exemplo de lógica para sugerir gestão de risco
            return {
                "stop_loss": "2% abaixo do preço atual",
                "stop_gain": "2% acima do preço atual",
                "tamanho_posicao": "Baseado no risco máximo por operação"
            }
    
        @staticmethod
        def executar_analise(simbolo: str, timeframe: str, indicadores: list, valor_banca: float, risco_por_operacao: float, data_final: str, estrategia: str = None, gestao_risco: dict = None):
            intervalo = timeframe_intervalo[timeframe]  # Define o intervalo com base no timeframe
    
            while True:
                if analises[id_analise]['pausada']:
                    time.sleep(1)  # Espera 1 segundo se a análise estiver pausada
                    continue
    
                # Mapear o timeframe para o formato do MetaTrader 5
                timeframe_map = {
                    "M1": mt5.TIMEFRAME_M1,
                    "H1": mt5.TIMEFRAME_H1,
                    "D1": mt5.TIMEFRAME_D1
                }
                mt5_timeframe = timeframe_map[timeframe]
    
                # Buscar dados do ativo usando MetaTrader 5
                try:
                    data_final_timestamp = int(datetime.strptime(data_final, "%Y-%m-%d").timestamp())
                    candles = mt5.copy_rates_from(simbolo, mt5_timeframe, datetime.now(), 365)
                    if candles is None:
                        print(f"Ativo {simbolo} não encontrado no MT5")
                        continue
    
                    df = pd.DataFrame(candles)
                    df['time'] = pd.to_datetime(df['time'], unit='s')
                    df = df[df['time'] <= datetime.strptime(data_final, "%Y-%m-%d")]  # Filtrar até a data final
                except Exception as e:
                    print(f"Erro ao buscar dados do ativo: {e}")
                    continue
    
                # Calcular indicadores solicitados
                for indicador in indicadores:
                    if indicador.startswith("SMA_"):
                        periodo = int(indicador.split("_")[1])
                        df[f"SMA_{periodo}"] = ta.sma(df['close'], length=periodo)
                    elif indicador.startswith("RSI_"):
                        periodo = int(indicador.split("_")[1])
                        df[f"RSI_{periodo}"] = ta.rsi(df['close'], length=periodo)
    
                # Preparar o prompt para a IA
                ultimo_fechamento = df.iloc[-1]['close']
                indicadores_str = ", ".join([f"{ind}: {df.iloc[-1][ind]}" for ind in indicadores])
    
                # Sugerir estratégia e gestão de risco se não forem fornecidos
                if not estrategia:
                    estrategia = AnaliseService.sugerir_estrategia(df)
                if not gestao_risco:
                    gestao_risco = AnaliseService.sugerir_gestao_risco(valor_banca, risco_por_operacao)
    
                # Calcular stop loss e stop gain com base na gestão de risco
                stop_loss, stop_gain, tamanho_posicao = AnaliseService.calcular_gestao_risco(valor_banca, risco_por_operacao, ultimo_fechamento)
    
                prompt = f"""
                Analise o ativo {simbolo} com base nos seguintes dados:
                - Último fechamento: {ultimo_fechamento}
                - Indicadores: {indicadores_str}
                - Valor da banca: {valor_banca}
                - Risco por operação: {risco_por_operacao}%
                - Estratégia sugerida: {estrategia}
                - Gestão de risco sugerida: {gestao_risco}
                - Stop Loss sugerido: {stop_loss}
                - Stop Gain sugerido: {stop_gain}
                - Tamanho da posição: {tamanho_posicao}
                Com base nesses dados, você recomendaria comprar, vender ou manter o ativo? Justifique sua resposta.
                """
    
                # Consultar o modelo de IA
                recomendacao_ia = consultar_ia(prompt)
    
                # Atualizar o resultado da análise
                analises[id_analise]['resultado'] = {
                    "simbolo": simbolo,
                    "timeframe": timeframe,
                    "ultimo_fechamento": ultimo_fechamento,
                    "indicadores": {ind: df.iloc[-1][ind] for ind in indicadores},
                    "estrategia": estrategia,
                    "gestao_risco": gestao_risco,
                    "stop_loss": stop_loss,
                    "stop_gain": stop_gain,
                    "tamanho_posicao": tamanho_posicao,
                    "recomendacao_ia": recomendacao_ia
                }
    
                # Aguardar o intervalo definido pelo timeframe
                time.sleep(intervalo)


---

#### 16. src/services/gestao_risco_service.py (Serviço de Gestão de Risco)
    from src.repositories.gestao_risco_repository import GestaoRiscoRepository
    
    class GestaoRiscoService:
        @staticmethod
        def criar_gestao_risco(db: Session, nome: str, descricao: str):
            return GestaoRiscoRepository.criar_gestao_risco(db, nome, descricao)
    
        @staticmethod
        def buscar_gestao_risco_por_id(db: Session, id: int):
            return GestaoRiscoRepository.buscar_gestao_risco_por_id(db, id)
    
        @staticmethod
        def atualizar_gestao_risco(db: Session, id: int, nome: str, descricao: str):
            return GestaoRiscoRepository.atualizar_gestao_risco(db, id, nome, descricao)
    
        @staticmethod
        def excluir_gestao_risco(db: Session, id: int):
            return GestaoRiscoRepository.excluir_gestao_risco(db, id)


---

#### 17. src/services/estrategia_service.py (Serviço de Estratégia)
    from src.repositories.estrategia_repository import EstrategiaRepository
    
    class EstrategiaService:
    
        @staticmethod
        def criar_estrategia(db: Session, nome: str, descricao: str):
            return EstrategiaRepository.criar_estrategia(db, nome, descricao)
    
        @staticmethod
        def buscar_estrategia_por_id(db: Session, id: int):
            return EstrategiaRepository.buscar_estrategia_por_id(db, id)
    
        @staticmethod
        def atualizar_estrategia(db: Session, id: int, nome: str, descricao: str):
            return EstrategiaRepository.atualizar_estrategia(db, id, nome, descricao)
    
        @staticmethod
        def excluir_estrategia(db: Session, id: int):
            return EstrategiaRepository.excluir_estrategia(db, id)


---

#### 18. src/controllers/usuario_controller.py (Controller de Usuários)
    from fastapi import APIRouter, Depends, HTTPException
    from sqlalchemy.orm import Session
    from src.models.usuario import UsuarioCreate, UsuarioLogin
    from src.services.usuario_service import UsuarioService
    from src.utils.auth import criar_token_jwt, ACCESS_TOKEN_EXPIRE_MINUTES
    from src.utils.database import get_db
    from datetime import timedelta
    
    router = APIRouter()
    
    @router.post("/cadastrar/", summary="Cadastrar um novo usuário")
    async def cadastrar_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
        try:
            UsuarioService.cadastrar_usuario(db, usuario.username, usuario.password)
            return {"mensagem": "Usuário cadastrado com sucesso!"}
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
    
    @router.post("/token/", summary="Obter token de autenticação")
    async def login(form_data: UsuarioLogin, db: Session = Depends(get_db)):
        try:
            usuario = UsuarioService.autenticar_usuario(db, form_data.username, form_data.password)
            access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
            access_token = criar_token_jwt(data={"sub": usuario.username}, expires_delta=access_token_expires)
            return {"access_token": access_token, "token_type": "bearer"}
        except ValueError as e:
            raise HTTPException(status_code=401, detail=str(e))


---

#### 19. src/controllers/analise_controller.py (Controller de Análise)
    from fastapi import APIRouter, Depends, HTTPException
    from sqlalchemy.orm import Session
    from src.models.analise import AnaliseRequest
    from src.services.analise_service import AnaliseService
    from src.utils.auth import obter_usuario_atual
    from src.utils.database import get_db
    import MetaTrader5 as mt5
    
    router = APIRouter()
    
    @router.post("/iniciar/", summary="Iniciar uma nova análise")
    async def iniciar_analise(analise: AnaliseRequest, usuario: dict = Depends(obter_usuario_atual), db: Session = Depends(get_db)):
        try:
            # Lógica para iniciar análise
            ...
            return {"id_analise": 1, "mensagem": "Análise iniciada com sucesso!"}
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
    
    @router.get("/timeframes/", summary="Listar timeframes disponíveis")
    async def listar_timeframes(usuario: dict = Depends(obter_usuario_atual)):
        # Timeframes disponíveis no MT5
        timeframes = {
            "M1": mt5.TIMEFRAME_M1,
            "M5": mt5.TIMEFRAME_M5,
            "M15": mt5.TIMEFRAME_M15,
            "H1": mt5.TIMEFRAME_H1,
            "H4": mt5.TIMEFRAME_H4,
            "D1": mt5.TIMEFRAME_D1,
            "W1": mt5.TIMEFRAME_W1,
            "MN1": mt5.TIMEFRAME_MN1
        }
        return timeframes
    
    @router.get("/indicadores/", summary="Listar indicadores disponíveis")
    async def listar_indicadores(usuario: dict = Depends(obter_usuario_atual)):
        # Lista de indicadores suportados (pode ser expandida)
        indicadores = [
            "SMA", "EMA", "RSI", "MACD", "Bollinger Bands",
            "Stochastic", "ATR", "ADX", "CCI", "Fibonacci"
        ]
        return indicadores


---

#### 20. src/controllers/gestao_risco_controller.py (Controller de Gestão de Risco)
    from fastapi import APIRouter, Depends, HTTPException
    from sqlalchemy.orm import Session
    from src.models.gestao_risco import GestaoRiscoCreate, GestaoRiscoUpdate
    from src.services.gestao_risco_service import GestaoRiscoService
    from src.utils.auth import obter_usuario_atual
    from src.utils.database import get_db
    
    router = APIRouter()
    
    @router.post("/", summary="Criar uma nova gestão de risco")
    async def criar_gestao_risco(gestao_risco: GestaoRiscoCreate, usuario: dict = Depends(obter_usuario_atual), db: Session = Depends(get_db)):
        try:
            GestaoRiscoService.criar_gestao_risco(db, gestao_risco.nome, gestao_risco.descricao)
            return {"mensagem": "Gestão de risco criada com sucesso!"}
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
    
    @router.get("/{id}", summary="Buscar uma gestão de risco por ID")
    async def buscar_gestao_risco(id: int, usuario: dict = Depends(obter_usuario_atual), db: Session = Depends(get_db)):
        gestao_risco = GestaoRiscoService.buscar_gestao_risco_por_id(db, id)
        if not gestao_risco:
            raise HTTPException(status_code=404, detail="Gestão de risco não encontrada")
        return gestao_risco
    
    @router.put("/{id}", summary="Atualizar uma gestão de risco")
    async def atualizar_gestao_risco(id: int, gestao_risco: GestaoRiscoUpdate, usuario: dict = Depends(obter_usuario_atual), db: Session = Depends(get_db)):
        try:
            GestaoRiscoService.atualizar_gestao_risco(db, id, gestao_risco.nome, gestao_risco.descricao)
            return {"mensagem": "Gestão de risco atualizada com sucesso!"}
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
    
    @router.delete("/{id}", summary="Excluir uma gestão de risco")
    async def excluir_gestao_risco(id: int, usuario: dict = Depends(obter_usuario_atual), db: Session = Depends(get_db)):
        try:
            GestaoRiscoService.excluir_gestao_risco(db, id)
            return {"mensagem": "Gestão de risco excluída com sucesso!"}
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))


---

#### 21. src/controllers/estrategia_controller.py (Controller de Estratégia)
    from fastapi import APIRouter, Depends, HTTPException
    from sqlalchemy.orm import Session
    from src.models.estrategia import EstrategiaCreate, EstrategiaUpdate
    from src.services.estrategia_service import EstrategiaService
    from src.utils.auth import obter_usuario_atual
    from src.utils.database import get_db
    
    router = APIRouter()
    
    @router.post("/", summary="Criar uma nova estratégia")
    async def criar_estrategia(estrategia: EstrategiaCreate, usuario: dict = Depends(obter_usuario_atual), db: Session = Depends(get_db)):
        try:
            EstrategiaService.criar_estrategia(db, estrategia.nome, estrategia.descricao)
            return {"mensagem": "Estratégia criada com sucesso!"}
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
    
    @router.get("/{id}", summary="Buscar uma estratégia por ID")
    async def buscar_estrategia(id: int, usuario: dict = Depends(obter_usuario_atual), db: Session = Depends(get_db)):
        estrategia = EstrategiaService.buscar_estrategia_por_id(db, id)
        if not estrategia:
            raise HTTPException(status_code=404, detail="Estratégia não encontrada")
        return estrategia
    
    @router.put("/{id}", summary="Atualizar uma estratégia")
    async def atualizar_estrategia(id: int, estrategia: EstrategiaUpdate, usuario: dict = Depends(obter_usuario_atual), db: Session = Depends(get_db)):
        try:
            EstrategiaService.atualizar_estrategia(db, id, estrategia.nome, estrategia.descricao)
            return {"mensagem": "Estratégia atualizada com sucesso!"}
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
    
    @router.delete("/{id}", summary="Excluir uma estratégia")
    async def excluir_estrategia(id: int, usuario: dict = Depends(obter_usuario_atual), db: Session = Depends(get_db)):
        try:
            EstrategiaService.excluir_estrategia(db, id)
            return {"mensagem": "Estratégia excluída com sucesso!"}
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))


---

#### 22. tests/conftest.py (Configurações Globais para os Testes)
    import pytest
    from fastapi.testclient import TestClient
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    from src.utils.database import Base
    from src.main import app
    from src.utils.database import get_db

    # Configuração do banco de dados de teste
    SQLALCHEMY_DATABASE_URL = "mysql+mysqlconnector://root:senha_segura@localhost/test_db"
    
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    # Cria as tabelas no banco de dados de teste
    Base.metadata.create_all(bind=engine)
    
    # Sobrescreve a dependência do banco de dados para usar o banco de teste
    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()
    
    app.dependency_overrides[get_db] = override_get_db
    
    @pytest.fixture(scope="module")
    def client():
        with TestClient(app) as client:
            yield client
    
    @pytest.fixture(scope="function")
    def db_session():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()


---

#### 23. tests/test_usuario.py (Testes para o Módulo de Usuários)
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


---

#### 24. tests/test_analise.py (Testes para o Módulo de Análises)
    import pytest
    from src.models.analise import AnaliseRequest
    from src.services.analise_service import AnaliseService
    from src.repositories.analise_repository import AnaliseRepository
    
    def test_criar_analise(db_session):
        # Testa a criação de uma análise
        analise = AnaliseRequest(
            simbolo="PETR4",
            timeframe="M1",
            valor_banca=10000.0,
            risco_por_operacao=1.0,
            data_final="2024-01-20"
        )
        nova_analise = AnaliseRepository.criar_analise(
            db_session,
            analise.simbolo,
            analise.timeframe,
            analise.valor_banca,
            analise.risco_por_operacao,
            analise.data_final,
            usuario_id=1
        )
        assert nova_analise.simbolo == "PETR4"
        assert nova_analise.timeframe == "M1"
        assert nova_analise.valor_banca == 10000.0
    
    def test_buscar_analise_por_id(db_session):
        # Testa a busca de uma análise por ID
        analise = AnaliseRequest(
            simbolo="PETR4",
            timeframe="M1",
            valor_banca=10000.0,
            risco_por_operacao=1.0,
            data_final="2024-01-20"
        )
        nova_analise = AnaliseRepository.criar_analise(
            db_session,
            analise.simbolo,
            analise.timeframe,
            analise.valor_banca,
            analise.risco_por_operacao,
            analise.data_final,
            usuario_id=1
        )
        analise_buscada = AnaliseRepository.buscar_analise_por_id(db_session, nova_analise.id)
        assert analise_buscada.id == nova_analise.id


---

#### 25. tests/test_gestao_risco.py (Testes para o Módulo de Gestão de Risco)
    import pytest
    from src.models.gestao_risco import GestaoRiscoCreate
    from src.services.gestao_risco_service import GestaoRiscoService
    from src.repositories.gestao_risco_repository import GestaoRiscoRepository
    
    def test_criar_gestao_risco(db_session):
        # Testa a criação de uma gestão de risco
        gestao_risco = GestaoRiscoCreate(nome="Risco Baixo", descricao="Risco de até 1%")
        nova_gestao_risco = GestaoRiscoService.criar_gestao_risco(db_session, gestao_risco.nome, gestao_risco.descricao)
        assert nova_gestao_risco.nome == "Risco Baixo"
        assert nova_gestao_risco.descricao == "Risco de até 1%"
    
    def test_buscar_gestao_risco_por_id(db_session):
        # Testa a busca de uma gestão de risco por ID
        gestao_risco = GestaoRiscoCreate(nome="Risco Baixo", descricao="Risco de até 1%")
        nova_gestao_risco = GestaoRiscoService.criar_gestao_risco(db_session, gestao_risco.nome, gestao_risco.descricao)
        gestao_risco_buscada = GestaoRiscoService.buscar_gestao_risco_por_id(db_session, nova_gestao_risco.id)
        assert gestao_risco_buscada.id == nova_gestao_risco.id


---

#### 26. tests/test_estrategia.py (Testes para o Módulo de Estratégias)
    import pytest
    from src.models.estrategia import EstrategiaCreate
    from src.services.estrategia_service import EstrategiaService
    from src.repositories.estrategia_repository import EstrategiaRepository
    
    def test_criar_estrategia(db_session):
        # Testa a criação de uma estratégia
        estrategia = EstrategiaCreate(nome="Tendência de Alta", descricao="Compra em tendência de alta")
        nova_estrategia = EstrategiaService.criar_estrategia(db_session, estrategia.nome, estrategia.descricao)
        assert nova_estrategia.nome == "Tendência de Alta"
        assert nova_estrategia.descricao == "Compra em tendência de alta"
    
    def test_buscar_estrategia_por_id(db_session):
        # Testa a busca de uma estratégia por ID
        estrategia = EstrategiaCreate(nome="Tendência de Alta", descricao="Compra em tendência de alta")
        nova_estrategia = EstrategiaService.criar_estrategia(db_session, estrategia.nome, estrategia.descricao)
        estrategia_buscada = EstrategiaService.buscar_estrategia_por_id(db_session, nova_estrategia.id)
        assert estrategia_buscada.id == nova_estrategia.id


---


### *Como Executar o Projeto*

*Execute os testes*:
   - No terminal, navegue até a pasta do projeto e execute: pytest tests/
   
1. *Crie os arquivos*: Copie e cole o conteúdo de cada arquivo em seu ambiente de desenvolvimento.
2. *Configure o Docker*:
   - No terminal, navegue até a pasta do projeto.
   - Execute docker-compose up --build para construir e iniciar os contêineres.
3. *Acesse a API*:
   - A API estará disponível em http://localhost:8000.
   - Acesse o Swagger UI em http://localhost:8000/docs.


---
