
import streamlit as st
import yfinance as yf
import pandas as pd
import datetime

st.set_page_config(layout="wide")
st.markdown("# 🎯 Ferramenta Sniper de Oportunidades - v1.1")
st.markdown("Esta ferramenta foca-se em encontrar **sinais exatos**, como um sniper. Apenas os ativos com justificativas fortes aparecerão.")

# Lista de ETFs ou ações
ativos = [
    "XAR", "ITA", "LMT", "BA", "RTX",
    "XLE", "XOP", "OIH", "PICK", "REMX",
    "LIT", "QQQ", "ARKK", "SOXX", "XLF"
]

# Função para verificar condições com .any()
def verificar_condicoes(data):
    try:
        data['RSI'] = ta.momentum.RSIIndicator(data['Close'], window=14).rsi()
        data['EMA50'] = ta.trend.EMAIndicator(data['Close'], window=50).ema_indicator()
        condicao = (data['RSI'] < 30) & (data['Close'] > data['EMA50'])
        return condicao.any()
    except Exception as e:
        return f"Erro ao calcular indicadores: {e}"

# Datas
fim = datetime.date.today()
inicio = fim - datetime.timedelta(days=180)

# Processamento
import ta  # garantir que 'ta' está disponível no ambiente

ativos_validos = []

for ticker in ativos:
    try:
        df = yf.download(ticker, start=inicio, end=fim)
        if df.empty:
            st.warning(f"Erro ao processar {ticker}: Dados vazios")
            continue

        resultado = verificar_condicoes(df)
        if isinstance(resultado, str):
            st.warning(f"Erro ao processar {ticker}: {resultado}")
        elif resultado:
            ativos_validos.append(ticker)

    except Exception as e:
        st.warning(f"Erro ao processar {ticker}: {e}")

if ativos_validos:
    st.success("🎯 Alvos identificados:")
    for a in ativos_validos:
        st.markdown(f"- **{a}**")
else:
    st.info("Nenhum alvo no momento. Sniper em espera...")
