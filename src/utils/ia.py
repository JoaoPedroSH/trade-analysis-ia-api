from fastapi import HTTPException
from openai import OpenAI, APIError, AuthenticationError
from dotenv import load_dotenv
import os

load_dotenv(override=True)

def enviar_prompt_ia():
    try:
        client = OpenAI(
            api_key=os.getenv("DEEPSEEK_API_KEY"), 
            base_url=os.getenv("DEEPSEEK_API_URL")
        )
        
        # EXEMPLO DE ENTRADA DO USUÁRIO
        
        # Ativo: BTC/USDT  
        # Base de Dados (últimos 14 dias):  
        # Data, Abertura, Máxima, Mínima, Fechamento, Volume  
        # 2023-10-01, 26500, 26800, 26300, 26750, 12000 BTC  
        # [...]  
        # 2023-10-14, 27200, 27500, 27000, 27400, 15000 BTC  
        # Timeframe: Diário (1D)  
        # Saldo: US$ 5.000  
        # Risco: 1%  
        # Price Action: suporte/resistência, padrão de triângulo ascendente  
        # Indicadores: RSI, Bandas de Bollinger  

        # O PROMPT VIRÁ POR PARÂMETRO
        response = client.chat.completions.create(
            model="deepseek-reasoner",
            messages=[
                {"role": "system", "content": "Você é um agente financeiro, especialista em price action e indicadores"},
                {"role": "user", "content": 
                 """
                    Solicito uma análise detalhada do ativo [INSIRA O NOME DO ATIVO, EX: BTC/USDT, PETR4.SA, ETC] com base nos seguintes dados:
                    
                    Base de Dados Histórica (formato CSV ou lista):
                    
                    Período: [EX: "Últimos 30 dias"]

                    Dados: [EX: Data, Abertura, Máxima, Mínima, Fechamento, Volume]
                    
                    Timeframe Analisado: [EX: Diário (1D), 1H, 15M]
                    
                    Saldo Disponível: [EX: RS10.000,00/US 2.000]
                    
                    Risco por Operação: [EX: 2% do saldo]
                    
                    Price Action Analisado (opcional): [EX: "suporte/resistência, padrões de candlestick, tendência"]
                    
                    Indicadores Técnicos (opcional): [EX: "RSI, MACD, Médias Móveis 50/200"]
                    
                    Instruções para a Análise:
                    
                    Analise price action com base nos critérios informados pelo usuário. Se não houver especificação, priorize suporte/resistência e tendência.
                    
                    Utilize os indicadores técnicos fornecidos. Se não houver escolha, aplique combinações clássicas (ex: RSI + Médias Móveis).
                    
                    Avalie volume, volatilidade e contexto do timeframe para definir a recomendação: COMPRAR, VENDER ou AGUARDAR.
                    
                    Em caso de compra/venda:
                    
                    Posicionamento: Calcule o tamanho da posição (risco vs saldo).
                    
                    Stop Loss (SL) e Take Profit (TP): Defina níveis com base em dados técnicos (ex: rompimento de suporte).
                    
                    Risco/Retorno: Indique a proporção esperada (ex: 1:2).
                    
                    Explique a lógica em 1 parágrafo, destacando indicadores-chave e padrões identificados.
                    
                    Mantenha a resposta objetiva e em ~300 tokens.
                """},
            ],
            temperature=0.7,
            max_tokens=200,
            stream=False
        )
        return { response.choices[0].message.content }
    
    except AuthenticationError as e:
        raise HTTPException(status_code=401, detail="Erro de autenticação: " + str(e))
    except APIError as e:
        raise HTTPException(status_code=500, detail="Erro na API: " + str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Erro inesperado: " + str(e))
