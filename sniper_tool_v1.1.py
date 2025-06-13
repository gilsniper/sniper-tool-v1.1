import streamlit as st
import yfinance as yf
import pandas as pd
import datetime

# Configuração da página
st.set_page_config(page_title="Sniper Tool v1.1", layout="wide")
st.title("🎯 Ferramenta Sniper de Oportunidades - v1.1")
st.markdown("Esta ferramenta foca-se em encontrar **sinais exatos**, como um sniper. Apenas os ativos com justificativas fortes aparecerão.")

# Lista de ativos a monitorizar (podes expandir)
symbols = [
    "XAR", "ITA", "LMT", "BA", "RTX",  # Defesa
    "XLE", "XOP", "OIH",              # Energia
    "PICK", "REMX", "LIT",            # Matérias-primas
    "QQQ", "ARKK", "SOXX", "XLF",     # Setores gerais e tech
]

# Datas
end = datetime.datetime.today()
start = end - datetime.timedelta(days=90)

# Resultados filtrados
sniper_hits = []

for symbol in symbols:
    try:
        data = yf.download(symbol, start=start, end=end)
        if data.empty:
            continue

        # Cálculo de volume médio e último volume
        avg_vol = data['Volume'].tail(20).mean()
        last_vol = data['Volume'].iloc[-1]

        # Cálculo de variação percentual recente
        close_now = data['Close'].iloc[-1]
        close_prev = data['Close'].iloc[-5]
        price_change = ((close_now - close_prev) / close_prev) * 100

        # Condições sniper
        if last_vol > avg_vol * 1.5 and price_change > 3:
            sniper_hits.append({
                "Ativo": symbol,
                "Preço atual": f"{close_now:.2f}",
                "Volume ↑": f"{last_vol/1e6:.2f}M",
                "Média 20 dias": f"{avg_vol/1e6:.2f}M",
                "Variação 5 dias": f"{price_change:.2f}%",
                "Justificação": "🚨 Aumento anormal de volume + valorização recente > 3%"
            })

    except Exception as e:
        st.warning(f"Erro ao processar {symbol}: {e}")

# Apresentação
if sniper_hits:
    st.success(f"🎯 {len(sniper_hits)} ativos com sinais de sniper encontrados:")
    st.dataframe(pd.DataFrame(sniper_hits))
else:
    st.info("Nenhum alvo no momento. Sniper em espera...")