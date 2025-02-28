import streamlit as st
import pandas as pd
import plotly.express as px

# Dados
meses = ["Dezembro", "Janeiro", "Fevereiro"]
dados = {
    "Mês": meses,
    "Contas com Engajamento": [59, 171, 286],
    "Seguidores": [476, 558, 728],
    "Alcance": [1322, 8778, 10096]
}
df = pd.DataFrame(dados)

# Configuração do Streamlit
st.set_page_config(page_title="BI Instagram", layout="wide")
st.title("📊 Dashboard Interativo - Instagram")

# Seleção de mês
mes_selecionado = st.selectbox("Selecione um mês", meses)

df_filtrado = df[df["Mês"] == mes_selecionado]

# Gráficos
col1, col2, col3 = st.columns(3)

with col1:
    fig1 = px.area(df, x="Mês", y="Contas com Engajamento", title="Contas com Engajamento", color_discrete_sequence=["royalblue"])
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    fig2 = px.area(df, x="Mês", y="Seguidores", title="Seguidores", color_discrete_sequence=["seagreen"])
    st.plotly_chart(fig2, use_container_width=True)

with col3:
    fig3 = px.area(df, x="Mês", y="Alcance", title="Alcance", color_discrete_sequence=["crimson"])
    st.plotly_chart(fig3, use_container_width=True)

# Exibir os dados filtrados
st.subheader("📌 Dados do Mês Selecionado")
st.write(df_filtrado)

st.markdown("Desenvolvido por Eduardo 🚀")        
