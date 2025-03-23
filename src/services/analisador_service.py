from sqlalchemy.orm import Session
import MetaTrader5 as mt5
import pandas as pd
from finta import TA
from datetime import datetime, timedelta
from src.repositories.analisador_repository import AnalisadorRepository
from src.utils.database import get_db
import yfinance as yf
import plotly.graph_objects as go


class AnalisadorService:
    @staticmethod
    def consultar_dados_analise(ticker, days, timeframe='1d'):
        """
        Função que obtém dados do ativo e gera gráfico de candlestick com indicadores
        
        Parâmetros:
        ticker (str): Símbolo do ativo
        days (int): Quantidade de dias para análise
        timeframe (str): Intervalo dos dados ('1m', '2m', '5m', '15m', '30m', '60m', '90m', '1h', '1d', '5d', '1wk', '1mo', '3mo')
        """
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        # Get stock data
        stock = yf.download(ticker, start=start_date, end=end_date, interval=timeframe)
        
        # Calculate indicators
        stock = AnalisadorService.calcular_indicadores(stock)
        
        # Handle MultiIndex columns
        def get_column_value(df, col):
            if isinstance(df[col], pd.DataFrame):
                return df[col].iloc[:, 0]
            return df[col]
        
        # Create figure
        fig = go.Figure()
        
        # Add candlesticks
        fig.add_trace(go.Candlestick(
            x=stock.index,
            open=get_column_value(stock, 'Open'),
            high=get_column_value(stock, 'High'),
            low=get_column_value(stock, 'Low'),
            close=get_column_value(stock, 'Close'),
            name='OHLC'
        ))
        
        # Add indicators
        fig.add_trace(go.Scatter(
            x=stock.index,
            y=get_column_value(stock, 'SMA20'),
            name='SMA 20',
            line=dict(color='orange')
        ))
        
        fig.add_trace(go.Scatter(
            x=stock.index,
            y=get_column_value(stock, 'SMA50'),
            name='SMA 50',
            line=dict(color='blue')
        ))
        
        # RSI
        fig.add_trace(go.Scatter(
            x=stock.index,
            y=get_column_value(stock, 'RSI'),
            name='RSI',
            yaxis="y2",
            line=dict(color='purple')
        ))
        
        # MACD
        fig.add_trace(go.Scatter(
            x=stock.index,
            y=get_column_value(stock, 'MACD'),
            name='MACD',
            yaxis="y3",
            line=dict(color='blue')
        ))
        
        fig.add_trace(go.Scatter(
            x=stock.index,
            y=get_column_value(stock, 'Signal_Line'),
            name='Signal Line',
            yaxis="y3",
            line=dict(color='red')
        ))
        
        # Update layout
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
        
        # Prepare response
        def get_value(df, col, agg_func=None):
            series = get_column_value(df, col)
            if agg_func:
                return float(agg_func(series))
            return float(series.iloc[-1])
        
        response = {
            'ticker': ticker,
            'period_days': days,
            'timeframe': timeframe,
            'current_price': get_value(stock, 'Close'),
            'highest_price': get_value(stock, 'High', max),
            'lowest_price': get_value(stock, 'Low', min),
            'volume': get_value(stock, 'Volume', sum),
            'start_date': start_date.strftime('%Y-%m-%d'),
            'end_date': end_date.strftime('%Y-%m-%d'),
            'current_rsi': get_value(stock, 'RSI'),
            'current_macd': get_value(stock, 'MACD'),
            'fig': fig
        }
        
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
    def executar_analise(analise: AnalisadorExecutar, db: Session):
        """
        Função que executa a análise em loop com base no timeframe.
        """
        try:
            # Mapeia o timeframe para o intervalo em segundos
            timeframe_intervalo = {
                "1m": 60,  # 1 minuto
                "5m": 300,  # 5 minutos
                "15m": 900,  # 15 minutos
                "30m": 1800,  # 30 minutos
            }

            intervalo = timeframe_intervalo.get(analise.timeframe, 60)  # Padrão: 1 minuto

            while analises_em_execucao[analise.ativo_financeiro]["executando"]:
                # Executa a análise
                resultado_dados = AnalisadorService.consultar_dados_analise(
                    analise.ativo_financeiro, 10, analise.timeframe
                )
                recomendacao_ia = AnalisadorService.executar_analise_ia(resultado_dados)

                # Salva o resultado no banco de dados ou realiza outras ações necessárias
                # Exemplo: registrar log no banco
                # AnalisadorService.registrar_resultado(db, analise, recomendacao_ia)

                print(f"Análise para {analise.ativo_financeiro} executada com sucesso!")

                # Aguarda o intervalo antes de executar novamente
                time.sleep(intervalo)

        except Exception as e:
            print(f"Erro ao executar análise para {analise.ativo_financeiro}: {e}")
        finally:
            # Marca a análise como parada
            analises_em_execucao[analise.ativo_financeiro]["executando"] = False
        
        
    @staticmethod
    def executar_analise_ia(dados):
        """
        Função que executa análise preditiva com IA
        """
        pass
            
