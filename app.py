import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# Configuração da página
st.set_page_config(page_title="BI Instagram", layout="wide", initial_sidebar_state="expanded")

# Função para carregar dados
@st.cache_data
def carregar_dados(arquivo=None):
    if arquivo is not None:
        try:
            # Carregar dados do arquivo CSV
            df = pd.read_csv(arquivo)
            
            # Verificar se as colunas necessárias existem
            colunas_necessarias = ["Mês", "Contas com Engajamento", "Seguidores", "Alcance", "Interações", "Curtidas", "Comentários"]
            colunas_faltantes = [col for col in colunas_necessarias if col not in df.columns]
            
            if colunas_faltantes:
                st.warning(f"Colunas faltantes no CSV: {', '.join(colunas_faltantes)}")
                st.info("Usando dados padrão. Certifique-se que seu CSV tem todas as colunas necessárias.")
                return carregar_dados_padrao()
                
        except Exception as e:
            st.error(f"Erro ao carregar arquivo: {e}")
            return carregar_dados_padrao()
    else:
        return carregar_dados_padrao()
    
    # Adicionar data para ordenação correta
    meses_num = {
        "Dezembro": datetime(2023, 12, 1),
        "Janeiro": datetime(2024, 1, 1),
        "Fevereiro": datetime(2024, 2, 1),
        "Março": datetime(2024, 3, 1),
        "Abril": datetime(2024, 4, 1),
        "Maio": datetime(2024, 5, 1),
        "Junho": datetime(2024, 6, 1)
    }
    
    try:
        df["Data"] = df["Mês"].map(meses_num)
        df = df.sort_values("Data")
        
        # Calcular métricas de crescimento
        df["Crescimento Seguidores"] = df["Seguidores"].pct_change() * 100
        df["Crescimento Alcance"] = df["Alcance"].pct_change() * 100
        df["Crescimento Engajamento"] = df["Contas com Engajamento"].pct_change() * 100
        
        # Taxa de engajamento
        df["Taxa de Engajamento"] = (df["Interações"] / df["Alcance"]) * 100
    except Exception as e:
        st.error(f"Erro ao processar dados: {e}")
        return carregar_dados_padrao()
    
    return df

def carregar_dados_padrao():
    # Dados padrão
    dados = {
        "Mês": ["Dezembro", "Janeiro", "Fevereiro"],
        "Contas com Engajamento": [59, 171, 286],
        "Seguidores": [476, 558, 728],
        "Alcance": [1322, 8778, 10096],
        "Interações": [125, 345, 587],
        "Curtidas": [95, 256, 432],
        "Comentários": [30, 89, 155]
    }
    df = pd.DataFrame(dados)
    
    # Adicionar data para ordenação correta
    meses_num = {
        "Dezembro": datetime(2023, 12, 1),
        "Janeiro": datetime(2024, 1, 1),
        "Fevereiro": datetime(2024, 2, 1)
    }
    df["Data"] = df["Mês"].map(meses_num)
    df = df.sort_values("Data")
    
    # Calcular métricas de crescimento
    df["Crescimento Seguidores"] = df["Seguidores"].pct_change() * 100
    df["Crescimento Alcance"] = df["Alcance"].pct_change() * 100
    df["Crescimento Engajamento"] = df["Contas com Engajamento"].pct_change() * 100
    
    # Taxa de engajamento
    df["Taxa de Engajamento"] = (df["Interações"] / df["Alcance"]) * 100
    
    return df

# Função para baixar arquivo CSV modelo
def baixar_csv_modelo():
    df_modelo = pd.DataFrame({
        "Mês": ["Dezembro", "Janeiro", "Fevereiro"],
        "Contas com Engajamento": [59, 171, 286],
        "Seguidores": [476, 558, 728],
        "Alcance": [1322, 8778, 10096],
        "Interações": [125, 345, 587],
        "Curtidas": [95, 256, 432],
        "Comentários": [30, 89, 155]
    })
    return df_modelo.to_csv(index=False).encode('utf-8')

# Sidebar para upload de arquivo
with st.sidebar:
    st.title("Filtros")
    uploaded_file = st.file_uploader("Carregar arquivo CSV", type="csv")
    
    # Adicionar opção para baixar CSV modelo
    st.download_button(
        label="📥 Baixar CSV modelo",
        data=baixar_csv_modelo(),
        file_name="modelo_instagram_dados.csv",
        mime="text/csv",
    )

# Carregar dados
if uploaded_file is not None:
    df = carregar_dados(uploaded_file)
else:
    df = carregar_dados()

# Continuação da sidebar após carregar os dados
with st.sidebar:
    mes_selecionado = st.selectbox("Selecione um mês", df["Mês"].tolist())
    st.divider()
    st.markdown("### Métricas Disponíveis")
    st.markdown("- Contas com Engajamento")
    st.markdown("- Seguidores")
    st.markdown("- Alcance")
    st.markdown("- Taxa de Engajamento")
    st.markdown("- Interações")

# Cabeçalho principal
st.title("📊 Dashboard Interativo - Instagram")
st.markdown("Análise de performance da conta no Instagram")

# Filtrar dados
df_filtrado = df[df["Mês"] == mes_selecionado]

# KPIs principais
st.subheader("📈 Indicadores de Desempenho")
col1, col2, col3, col4 = st.columns(4)

with col1:
    seguidores_atual = int(df_filtrado["Seguidores"].values[0])
    if mes_selecionado != "Dezembro":
        crescimento = float(df_filtrado["Crescimento Seguidores"].values[0])
        st.metric("Seguidores", f"{seguidores_atual}", f"{crescimento:.1f}%")
    else:
        st.metric("Seguidores", f"{seguidores_atual}", "")

with col2:
    alcance_atual = int(df_filtrado["Alcance"].values[0])
    if mes_selecionado != "Dezembro":
        crescimento = float(df_filtrado["Crescimento Alcance"].values[0])
        st.metric("Alcance", f"{alcance_atual}", f"{crescimento:.1f}%")
    else:
        st.metric("Alcance", f"{alcance_atual}", "")

with col3:
    engajamento_atual = int(df_filtrado["Contas com Engajamento"].values[0])
    if mes_selecionado != "Dezembro":
        crescimento = float(df_filtrado["Crescimento Engajamento"].values[0])
        st.metric("Contas Engajadas", f"{engajamento_atual}", f"{crescimento:.1f}%")
    else:
        st.metric("Contas Engajadas", f"{engajamento_atual}", "")

with col4:
    taxa_engaj = float(df_filtrado["Taxa de Engajamento"].values[0])
    st.metric("Taxa de Engajamento", f"{taxa_engaj:.2f}%")

# Gráficos de tendência
st.subheader("📉 Tendências Mensais")
col1, col2 = st.columns(2)

with col1:
    # Gráfico de seguidores com linha de tendência
    fig1 = px.line(df, x="Mês", y="Seguidores", markers=True, 
                 title="Crescimento de Seguidores",
                 color_discrete_sequence=["seagreen"])
    fig1.add_trace(go.Scatter(x=df["Mês"], y=df["Seguidores"], 
                          mode='lines', name='Tendência',
                          line=dict(color='seagreen', dash='dash')))
    # Destacar o mês selecionado
    mes_idx = df.index[df["Mês"] == mes_selecionado].tolist()[0]
    fig1.add_trace(go.Scatter(x=[df.iloc[mes_idx]["Mês"]], 
                              y=[df.iloc[mes_idx]["Seguidores"]],
                              mode='markers',
                              marker=dict(color='red', size=12),
                              name=mes_selecionado))
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    # Gráfico de alcance
    fig2 = px.line(df, x="Mês", y="Alcance", markers=True,
                 title="Evolução do Alcance",
                 color_discrete_sequence=["royalblue"])
    fig2.add_trace(go.Scatter(x=df["Mês"], y=df["Alcance"], 
                          mode='lines', name='Tendência',
                          line=dict(color='royalblue', dash='dash')))
    # Destacar o mês selecionado
    fig2.add_trace(go.Scatter(x=[df.iloc[mes_idx]["Mês"]], 
                              y=[df.iloc[mes_idx]["Alcance"]],
                              mode='markers',
                              marker=dict(color='red', size=12),
                              name=mes_selecionado))
    st.plotly_chart(fig2, use_container_width=True)

# Gráfico de barras de engajamento
st.subheader("🔍 Análise de Engajamento")
col1, col2 = st.columns(2)

with col1:
    # Comparativo de interações
    fig3 = px.bar(df, x="Mês", y=["Curtidas", "Comentários"], 
                title="Interações por Mês",
                barmode='group')
    st.plotly_chart(fig3, use_container_width=True)

with col2:
    # Taxa de engajamento
    fig4 = px.line(df, x="Mês", y="Taxa de Engajamento", markers=True,
                 title="Taxa de Engajamento (%)",
                 color_discrete_sequence=["crimson"])
    st.plotly_chart(fig4, use_container_width=True)

# Tabela de dados detalhados
st.subheader("📌 Dados Detalhados")
colunas_exibir = ["Mês", "Seguidores", "Alcance", "Contas com Engajamento", 
                 "Taxa de Engajamento", "Interações", "Curtidas", "Comentários"]
st.dataframe(df_filtrado[colunas_exibir], use_container_width=True)

# Rodapé
st.divider()
st.markdown("Desenvolvido por Eduardo 🚀 | Última atualização: Fevereiro 2024")
