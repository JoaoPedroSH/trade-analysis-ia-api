import MetaTrader5 as mt5
import pandas as pd
import pandas_ta as ta
from datetime import datetime
from src.repositories.analisador_repository import AnalisadorRepository
from src.utils.database import get_db

class AnalisadorService:
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
    def executar_analisador(simbolo: str, timeframe: str, indicadores: list, valor_banca: float, risco_por_operacao: float, data_final: str, estrategia: str = None, gestao_risco: dict = None):
        intervalo = timeframe_intervalo[timeframe]  # Define o intervalo com base no timeframe

        while True:
            if analisadores[id_analisador]['pausada']:
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
            analisadores[id_analisador]['resultado'] = {
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
