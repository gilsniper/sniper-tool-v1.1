
import streamlit as st
from scraper import get_live_contracts
import pandas as pd
import yfinance as yf
import datetime

st.set_page_config(page_title="Radar Sniper Reconstrução v1.1+", layout="wide")
st.title("🏗️ Radar Sniper Reconstrução Pós-Guerra v1.1+")

st.markdown("""
Este radar consulta fontes REAIS de press releases + Google News para identificar contratos de reconstrução em países pós-conflito (ex: Ucrânia, Israel).

**Atualização automática:** a cada 5 minutos.
""")

# Obter contratos reais do scraper
contratos = get_live_contracts()

# Mostrar contratos
st.subheader("🔎 Contratos Identificados em Tempo Real")
if contratos:
    df = pd.DataFrame(contratos)
    df['Link'] = df['Link'].apply(lambda x: f"[Abrir]({x})")
    st.dataframe(df, use_container_width=True)
else:
    st.info("Nenhum contrato detectado no momento. Radar em vigia...")

# Contexto preço & volume
st.subheader("📈 Contexto de Preço & Volume")
empresas = [c['Empresa'] for c in contratos if c['Empresa'] != "Google News"]
if not empresas:
    empresas = ["FLR", "KBR", "J", "ACM", "PWR", "CAT", "DE", "VMC", "MLM"]  # fallback

period = "1mo"
end = datetime.date.today()
start = end - datetime.timedelta(days=30)
data = yf.download(empresas, start=start, end=end, interval="1d", group_by='ticker', progress=False)

for ticker in empresas:
    try:
        last = data[ticker].iloc[-1]
        st.write(f"**{ticker}** — Preço: ${last['Close']:.2f} | Volume: {last['Volume']:,}")
    except:
        st.write(f"**{ticker}** — Dados indisponíveis")
