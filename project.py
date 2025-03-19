from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
import mysql.connector
import MetaTrader5 as mt5
import pandas as pd
import pandas_ta as ta
from transformers import pipeline
import threading
import time

# Configuração do FastAPI
app = FastAPI()

# Configuração do banco de dados
db_config = {
    'host': 'localhost',
    'user': 'seu_usuario',
    'password': 'sua_senha',
    'database': 'mercado_financeiro'
}

# Configuração do JWT
SECRET_KEY = "sua_chave_secreta"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Configuração de segurança
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Inicializar o MetaTrader 5
if not mt5.initialize():
    raise Exception("Falha ao inicializar o MetaTrader 5")

# Carregar o modelo do Hugging Face
model_name = "google/flan-t5-large"  # Escolha o modelo desejado
gerador_texto = pipeline("text2text-generation", model=model_name)

# Dicionário para armazenar análises
analises = {}

# Mapeamento de timeframe para intervalo em segundos
timeframe_intervalo = {
    "M1": 60,  # 1 minuto
    "H1": 3600,  # 1 hora
    "D1": 86400  # 1 dia
}


# Modelo de dados para receber os dados do usuário
class AnaliseRequest(BaseModel):
    simbolo: str
    timeframe: str  # Ex.: "M1", "H1", "D1"
    indicadores: list  # Ex.: ["SMA_20", "RSI_14"]
    valor_banca: float  # Valor da banca do usuário
    risco_por_operacao: float  # Ex.: 1.0 (1% do capital)
    data_final: str  # Ex.: "2024-01-20"


# Modelo de dados para cadastro de usuário
class UsuarioCreate(BaseModel):
    username: str
    password: str


# Modelo de dados para login
class UsuarioLogin(BaseModel):
    username: str
    password: str


# Função para conectar ao banco de dados
def get_db_connection():
    return mysql.connector.connect(**db_config)


# Função para verificar a senha
def verificar_senha(senha_plana, senha_hash):
    return pwd_context.verify(senha_plana, senha_hash)


# Função para gerar o hash da senha
def gerar_hash_senha(senha):
    return pwd_context.hash(senha)


# Função para criar token JWT
def criar_token_jwt(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# Função para autenticar usuário
def autenticar_usuario(username: str, password: str):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM usuarios WHERE username = %s", (username,))
    usuario = cursor.fetchone()
    cursor.close()
    conn.close()

    if not usuario or not verificar_senha(password, usuario['password_hash']):
        return None
    return usuario


# Função para obter o usuário atual
async def obter_usuario_atual(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Token inválido")
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido")

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM usuarios WHERE username = %s", (username,))
    usuario = cursor.fetchone()
    cursor.close()
    conn.close()

    if usuario is None:
        raise HTTPException(status_code=401, detail="Usuário não encontrado")
    return usuario


# Rota para cadastrar usuário
@app.post("/usuarios/cadastrar/")
async def cadastrar_usuario(usuario: UsuarioCreate):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE username = %s", (usuario.username,))
    if cursor.fetchone():
        raise HTTPException(status_code=400, detail="Usuário já existe")

    hashed_password = gerar_hash_senha(usuario.password)
    cursor.execute("INSERT INTO usuarios (username, password_hash) VALUES (%s, %s)",
                   (usuario.username, hashed_password))
    conn.commit()
    cursor.close()
    conn.close()

    return {"mensagem": "Usuário cadastrado com sucesso!"}


# Rota para login e obter token JWT
@app.post("/token/")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    usuario = autenticar_usuario(form_data.username, form_data.password)
    if not usuario:
        raise HTTPException(status_code=401, detail="Usuário ou senha incorretos")

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = criar_token_jwt(data={"sub": usuario['username']}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}


# Função para calcular stop loss e stop gain com base na gestão de risco
def calcular_gestao_risco(valor_banca, risco_por_operacao, preco_atual):
    risco_maximo = valor_banca * (risco_por_operacao / 100)
    stop_loss = preco_atual * 0.98  # Exemplo: 2% abaixo do preço atual
    stop_gain = preco_atual * 1.02  # Exemplo: 2% acima do preço atual
    tamanho_posicao = risco_maximo / (preco_atual - stop_loss)
    return stop_loss, stop_gain, tamanho_posicao


# Rota para iniciar uma nova análise
@app.post("/analise/iniciar/")
async def iniciar_analise(analise: AnaliseRequest, usuario: dict = Depends(obter_usuario_atual)):
    id_analise = len(analises) + 1
    analises[id_analise] = {
        "pausada": False,
        "resultado": None,
        "thread": threading.Thread(target=executar_analise, args=(
            id_analise,
            analise.simbolo,
            analise.timeframe,
            analise.indicadores,
            analise.valor_banca,
            analise.risco_por_operacao,
            analise.data_final
        ))
    }
    analises[id_analise]['thread'].start()

    # Registrar log
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO logs (usuario_id, acao) VALUES (%s, %s)",
                   (usuario['id'], f"Iniciou análise {id_analise}"))
    conn.commit()
    cursor.close()
    conn.close()

    return {"id_analise": id_analise, "mensagem": "Análise iniciada com sucesso!"}


# Função para executar a análise em loop
def executar_analise(id_analise, simbolo, timeframe, indicadores, valor_banca, risco_por_operacao, data_final):
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

        # Calcular stop loss e stop gain com base na gestão de risco
        stop_loss, stop_gain, tamanho_posicao = calcular_gestao_risco(valor_banca, risco_por_operacao,
                                                                      ultimo_fechamento)

        prompt = f"""
        Analise o ativo {simbolo} com base nos seguintes dados:
        - Último fechamento: {ultimo_fechamento}
        - Indicadores: {indicadores_str}
        - Valor da banca: {valor_banca}
        - Risco por operação: {risco_por_operacao}%
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
            "stop_loss": stop_loss,
            "stop_gain": stop_gain,
            "tamanho_posicao": tamanho_posicao,
            "recomendacao_ia": recomendacao_ia
        }

        # Aguardar o intervalo definido pelo timeframe
        time.sleep(intervalo)


# Rota para pausar uma análise
@app.post("/analise/pausar/{id_analise}")
async def pausar_analise(id_analise: int, usuario: dict = Depends(obter_usuario_atual)):
    if id_analise not in analises:
        raise HTTPException(status_code=404, detail="Análise não encontrada")
    analises[id_analise]['pausada'] = True

    # Registrar log
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO logs (usuario_id, acao) VALUES (%s, %s)",
                   (usuario['id'], f"Pausou análise {id_analise}"))
    conn.commit()
    cursor.close()
    conn.close()

    return {"mensagem": f"Análise {id_analise} pausada com sucesso!"}


# Rota para retomar uma análise
@app.post("/analise/retomar/{id_analise}")
async def retomar_analise(id_analise: int, usuario: dict = Depends(obter_usuario_atual)):
    if id_analise not in analises:
        raise HTTPException(status_code=404, detail="Análise não encontrada")
    analises[id_analise]['pausada'] = False

    # Registrar log
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO logs (usuario_id, acao) VALUES (%s, %s)",
                   (usuario['id'], f"Retomou análise {id_analise}"))
    conn.commit()
    cursor.close()
    conn.close()

    return {"mensagem": f"Análise {id_analise} retomada com sucesso!"}


# Rota para obter o resultado de uma análise
@app.get("/analise/resultado/{id_analise}")
async def obter_resultado(id_analise: int, usuario: dict = Depends(obter_usuario_atual)):
    if id_analise not in analises:
        raise HTTPException(status_code=404, detail="Análise não encontrada")

    # Registrar log
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO logs (usuario_id, acao) VALUES (%s, %s)",
                   (usuario['id'], f"Consultou resultado da análise {id_analise}"))
    conn.commit()
    cursor.close()
    conn.close()

    return analises[id_analise]['resultado']


# Iniciar o servidor
if _name_ == "_main_":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)