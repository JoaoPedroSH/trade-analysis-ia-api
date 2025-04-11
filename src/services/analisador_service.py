import pandas as pd
from datetime import datetime, timedelta
from src.models.analisador import AnalisadorExecutar
import yfinance as yf
import plotly.graph_objects as go
from src.utils.celery_app import celery_app
from src.utils.ia import enviar_prompt_ia
import MetaTrader5 as mt5
import plotly.graph_objects as go
from ta.trend import SMAIndicator, MACD
from ta.momentum import RSIIndicator
from datetime import datetime, timedelta
import json

class AnalisadorService:
    @staticmethod
    def consultar_dados_analise(ticker, days, timeframe='1d'):
        """
        Obtém dados via MetaTrader 5 e gera gráfico com indicadores.
        """
        # Inicializa o MetaTrader
        if not mt5.initialize():
            raise RuntimeError("Não foi possível iniciar o MetaTrader 5")

        # Mapeamento do timeframe
        tf_map = {
            '1m': mt5.TIMEFRAME_M1,
            '5m': mt5.TIMEFRAME_M5,
            '15m': mt5.TIMEFRAME_M15,
            '30m': mt5.TIMEFRAME_M30,
            '1h': mt5.TIMEFRAME_H1,
            '1d': mt5.TIMEFRAME_D1,
        }

        if timeframe not in tf_map:
            raise ValueError(f"Timeframe '{timeframe}' não suportado para MetaTrader 5")

        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)

        # Pega os dados históricos
        rates = mt5.copy_rates_range(ticker, tf_map[timeframe], start_date, end_date)
        if rates is None or len(rates) == 0:
            raise RuntimeError(f"Nenhum dado retornado para o ativo {ticker}")

        df = pd.DataFrame(rates)
        df['time'] = pd.to_datetime(df['time'])
        df.set_index('time', inplace=True)
        df.rename(columns={'open': 'Open', 'high': 'High', 'low': 'Low', 'close': 'Close', 'tick_volume': 'Volume'}, inplace=True)

        # Indicadores
        df['SMA20'] = SMAIndicator(df['Close'], window=20).sma_indicator()
        df['SMA50'] = SMAIndicator(df['Close'], window=50).sma_indicator()
        df['RSI'] = RSIIndicator(df['Close']).rsi()

        macd = MACD(df['Close'])
        df['MACD'] = macd.macd()
        df['Signal_Line'] = macd.macd_signal()

        # Função auxiliar
        def get_column_value(df, col):
            return df[col]

        # Gráfico
        fig = go.Figure()
        fig.add_trace(go.Candlestick(
            x=df.index,
            open=df['Open'],
            high=df['High'],
            low=df['Low'],
            close=df['Close'],
            name='OHLC'
        ))
        fig.add_trace(go.Scatter(x=df.index, y=df['SMA20'], name='SMA 20', line=dict(color='orange')))
        fig.add_trace(go.Scatter(x=df.index, y=df['SMA50'], name='SMA 50', line=dict(color='blue')))
        fig.add_trace(go.Scatter(x=df.index, y=df['RSI'], name='RSI', yaxis="y2", line=dict(color='purple')))
        fig.add_trace(go.Scatter(x=df.index, y=df['MACD'], name='MACD', yaxis="y3", line=dict(color='blue')))
        fig.add_trace(go.Scatter(x=df.index, y=df['Signal_Line'], name='Signal Line', yaxis="y3", line=dict(color='red')))

        fig.update_layout(
            title=f'Análise Técnica - {ticker} ({timeframe})',
            yaxis_title='Preço',
            xaxis_title='Data',
            template='plotly_dark',
            yaxis=dict(domain=[0.3, 1.0]),
            yaxis2=dict(domain=[0.15, 0.28], title='RSI'),
            yaxis3=dict(domain=[0, 0.13], title='MACD'),
            xaxis=dict(rangeslider=dict(visible=False))
        )

        # Prepara resposta
        def get_value(df, col, agg_func=None):
            series = get_column_value(df, col)
            if agg_func:
                return float(agg_func(series.dropna()))
            return float(series.dropna().iloc[-1])

        response = {
            'ticker': ticker,
            'period_days': days,
            'timeframe': timeframe,
            'current_price': get_value(df, 'Close'),
            'highest_price': get_value(df, 'High', max),
            'lowest_price': get_value(df, 'Low', min),
            'volume': get_value(df, 'Volume', sum),
            'start_date': start_date.strftime('%Y-%m-%d'),
            'end_date': end_date.strftime('%Y-%m-%d'),
            'current_rsi': get_value(df, 'RSI'),
            'current_macd': get_value(df, 'MACD'),
            'fig': fig
        }

        mt5.shutdown()
        return response
    
    @staticmethod
    def calcular_indicadores(stock_data):
        """
        Calcula indicadores técnicos
        """
        # Handle MultiIndex DataFrame
        close_col = stock_data['Close'].iloc[:, 0] if isinstance(stock_data['Close'], pd.DataFrame) else stock_data['Close']
        
        # Create working DataFrame
        df = pd.DataFrame(close_col)
        df.columns = ['Close']
        
        # Calculate indicators
        df['SMA20'] = df['Close'].rolling(window=20).mean()
        df['SMA50'] = df['Close'].rolling(window=50).mean()
        
        # RSI
        delta = df['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        df['RSI'] = 100 - (100 / (1 + rs))
        
        # MACD
        exp1 = df['Close'].ewm(span=12, adjust=False).mean()
        exp2 = df['Close'].ewm(span=26, adjust=False).mean()
        df['MACD'] = exp1 - exp2
        df['Signal_Line'] = df['MACD'].ewm(span=9, adjust=False).mean()
        
        # Create a new DataFrame with the same index as stock_data
        indicators_df = pd.DataFrame(index=stock_data.index)
        
        # Add indicators to the new DataFrame
        for col in df.columns:
            if col != 'Close':
                if isinstance(stock_data.columns, pd.MultiIndex):
                    indicators_df[(col, stock_data.columns.get_level_values(1)[0])] = df[col].values
                else:
                    indicators_df[col] = df[col].values
        
        # Combine the original stock_data with indicators
        result = pd.concat([stock_data, indicators_df], axis=1)
        return result
    
    @staticmethod
    @celery_app.task(bind=True)
    def executar_analise(self, analise: AnalisadorExecutar):
        try:
            dados_analise = AnalisadorService.consultar_dados_analise(analise.ativo_financeiro, analise.periodo_analise_dados, analise.timeframe)
            analise.dados_historicos = dados_analise['fig'].to_json()
            prompt = AnalisadorService.montar_prompt(analise)
            resposta_ia = enviar_prompt_ia(prompt)
            
            return {
                'ticker': dados_analise['ticker'],
                'current_price': dados_analise['current_price'],
                'highest_price': dados_analise['highest_price'],
                'lowest_price': dados_analise['lowest_price'],
                'volume': dados_analise['volume'],
                'indicadores': {
                    'current_rsi': dados_analise['current_rsi'],
                    'current_macd': dados_analise['current_macd'],
                },
                'fig': dados_analise['fig'].to_json(),
                'analise': resposta_ia
            }
        except Exception as e:
            raise e
            
    @staticmethod
    def montar_prompt(dados: AnalisadorExecutar):
        return [
                {"role": "system", "content": "Você é um agente financeiro, especialista em price action e indicadores, que dá dicas para entusiastas"},
                {"role": "user", "content": 
                 f"""
                    Solicito uma análise técnica detalhada do ativo {dados.ativo_financeiro} com base nos seguintes parâmetros:
                    Dados Históricos: {dados.dados_historicos}
                    Formato dos Dados: Data, Abertura, Máxima, Mínima, Fechamento, Volume
                    Período: Últimos {dados.periodo_analise_dados} dias
                    Timeframe: {dados.timeframe}
                    Saldo Disponível: {dados.saldo}
                    Risco por Operação: {dados.risco}
                    Price Action: {dados.price_action}
                    Indicadores Técnicos: {dados.indicadores}
                    Instruções:
                    Analise o price action com base nas instruções fornecidas. Se não houver, considere suporte, resistência e tendência.
                    Aplique os indicadores informados; se não houver, utilize Médias Móveis.
                    Avalie volume, volatilidade, contexto do timeframe e convergência entre indicadores e price action.
                    Conclua com uma recomendação: COMPRAR, VENDER ou AGUARDAR.
                    Em caso de sinal de entrada:
                    Calcule o tamanho da posição (risco vs saldo).
                    Defina SL e TP com base em níveis técnicos.
                    Informe o risco/retorno esperado (ex: 1:2).
                    Explique a lógica em um parágrafo, destacando os principais sinais da análise.
                    Limite: resposta objetiva com cerca de 300 tokens.
                """},
            ]
