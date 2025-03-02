import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# Configuração da página
st.set_page_config(page_title="BI Instagram", layout="wide", initial_sidebar_state="expanded")

if st.sidebar.button("🔄 Recarregar Dados"):
    st.cache_data.clear()
    st.rerun()
    
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
            
            # Continuar com o processamento se o CSV estiver correto
            return processar_dados(df)
                
        except Exception as e:
            st.error(f"Erro ao carregar arquivo: {e}")
            return carregar_dados_padrao()
    else:
        return carregar_dados_padrao()

def carregar_dados_padrao():
    df_padrao = pd.DataFrame({
        "Mês": ["Dez/24", "Jan/25", "Fev/25"],
        "Contas com Engajamento": [59, 171, 286],
        "Seguidores": [9052, 9169, 9347],
        "Alcance": [193936, 86329, 132230],
        "Interações": [646, 491, 1283],
        "Curtidas": [216, 130, 399],
        "Comentários": [5, 0, 22]
        "Visualizações": [382379, 257898, 489698]
    })
    return processar_dados(df_padrao)

def processar_dados(df):
    # Adicionar data para ordenação correta
    # Mapear nomes de meses para datas reais para ordenação correta
    meses_mapeamento = {
        # 2023
        "Dez/23": datetime(2023, 12, 1),
        "Dezembro": datetime(2023, 12, 1),
        "Dezembro 2023": datetime(2023, 12, 1),
        
        # 2024
        "Jan/24": datetime(2024, 1, 1),
        "Janeiro": datetime(2024, 1, 1),
        "Janeiro 2024": datetime(2024, 1, 1),
        
        "Fev/24": datetime(2024, 2, 1),
        "Fevereiro": datetime(2024, 2, 1),
        "Fevereiro 2024": datetime(2024, 2, 1),
        
        "Mar/24": datetime(2024, 3, 1),
        "Março": datetime(2024, 3, 1),
        "Março 2024": datetime(2024, 3, 1),
        
        "Abr/24": datetime(2024, 4, 1),
        "Abril": datetime(2024, 4, 1),
        "Abril 2024": datetime(2024, 4, 1),
        
        "Mai/24": datetime(2024, 5, 1),
        "Maio": datetime(2024, 5, 1),
        "Maio 2024": datetime(2024, 5, 1),
        
        "Jun/24": datetime(2024, 6, 1),
        "Junho": datetime(2024, 6, 1),
        "Junho 2024": datetime(2024, 6, 1),
        
        "Jul/24": datetime(2024, 7, 1),
        "Julho": datetime(2024, 7, 1),
        "Julho 2024": datetime(2024, 7, 1),
        
        "Ago/24": datetime(2024, 8, 1),
        "Agosto": datetime(2024, 8, 1),
        "Agosto 2024": datetime(2024, 8, 1),
        
        "Set/24": datetime(2024, 9, 1),
        "Setembro": datetime(2024, 9, 1),
        "Setembro 2024": datetime(2024, 9, 1),
        
        "Out/24": datetime(2024, 10, 1),
        "Outubro": datetime(2024, 10, 1),
        "Outubro 2024": datetime(2024, 10, 1),
        
        "Nov/24": datetime(2024, 11, 1),
        "Novembro": datetime(2024, 11, 1),
        "Novembro 2024": datetime(2024, 11, 1),
        
        "Dez/24": datetime(2024, 12, 1),
        "Dezembro 2024": datetime(2024, 12, 1)
    }
    
    try:
        # Criar coluna de data para ordenação
        df["Data"] = df["Mês"].map(meses_mapeamento)
        df = df.sort_values("Data")
        
        # Garantir que todas as colunas numéricas sejam do tipo float para evitar erros
        colunas_numericas = ["Contas com Engajamento", "Seguidores", "Alcance", "Interações", "Curtidas", "Comentários", "visualizações"]
        for col in colunas_numericas:
            df[col] = pd.to_numeric(df[col], errors='coerce')
        
        # Calcular métricas de crescimento (exceto para o primeiro mês)
        df["Crescimento Seguidores"] = df["Seguidores"].pct_change() * 100
        df["Crescimento Alcance"] = df["Alcance"].pct_change() * 100
        df["Crescimento Engajamento"] = df["Contas com Engajamento"].pct_change() * 100
        
        # Taxa de engajamento
        df["Taxa de Engajamento"] = (df["Interações"] / df["Alcance"]) * 100
    except Exception as e:
        st.error(f"Erro ao processar dados: {e}")
        return pd.DataFrame()
    
    return df

# Função para baixar arquivo CSV modelo
def baixar_csv_modelo():
    df_modelo = pd.DataFrame({
        "Mês": ["Dez/24", "Jan/25", "Fev/25"],
        "Contas com Engajamento": [59, 171, 286],
        "Seguidores": [9052, 9169, 9347],
        "Alcance": [193936, 86329, 132230],
        "Interações": [646, 491, 1283],
        "Curtidas": [216, 130, 399],
        "Comentários": [5, 0, 22]
        "Visualizações": [2500, 3200, 4100]
    })
    return df_modelo.to_csv(index=False).encode('utf-8')

# Verificar se as colunas necessárias existem
colunas_necessarias = ["Mês", "Contas com Engajamento", "Seguidores", "Alcance", "Interações", "Curtidas", "Comentários", "Visualizações"]


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

# Continuação da sidebar após carregar os dados (APENAS UM with st.sidebar)
with st.sidebar:
    mes_selecionado = st.selectbox("Selecione um mês", df["Mês"].tolist())
    st.divider()
    st.markdown("### Métricas Disponíveis")
    st.markdown("- Contas com Engajamento")
    st.markdown("- Seguidores")
    st.markdown("- Alcance")
    st.markdown("- Taxa de Engajamento")
    st.markdown("- Interações")
    st.markdown("- Visualizações")
    
# Cabeçalho principal
st.title("📊 Dashboard Interativo - Elétrica Paraná")
st.markdown("Análise de performance da conta no Instagram")

# Filtrar dados
df_filtrado = df[df["Mês"] == mes_selecionado]

# Função para formatar números grandes
def formatar_numero(numero):
    if numero >= 1000:
        return f"{numero/1000:.1f}k"
    return f"{numero}"
        
# KPIs principais
st.subheader("📈 Indicadores de Desempenho")
col1, col2, col3, col4, col5 = st.columns(5)

# Verificar se é o primeiro mês (não mostrar crescimento)
primeiro_mes = df.iloc[0]["Mês"]

with col1:
    seguidores_atual = int(df_filtrado["Seguidores"].values[0])
    if mes_selecionado != primeiro_mes and not pd.isna(df_filtrado["Crescimento Seguidores"].values[0]):
        crescimento = float(df_filtrado["Crescimento Seguidores"].values[0])
        st.metric("Seguidores", formatar_numero(seguidores_atual), f"{crescimento:.1f}%")
    else:
        st.metric("Seguidores", formatar_numero(seguidores_atual), "")

with col2:
    alcance_atual = int(df_filtrado["Alcance"].values[0])
    if mes_selecionado != primeiro_mes and not pd.isna(df_filtrado["Crescimento Alcance"].values[0]):
        crescimento = float(df_filtrado["Crescimento Alcance"].values[0])
        st.metric("Alcance", formatar_numero(alcance_atual), f"{crescimento:.1f}%")
    else:
        st.metric("Alcance", formatar_numero(alcance_atual), "")

with col3:
    engajamento_atual = int(df_filtrado["Contas com Engajamento"].values[0])
    if mes_selecionado != primeiro_mes and not pd.isna(df_filtrado["Crescimento Engajamento"].values[0]):
        crescimento = float(df_filtrado["Crescimento Engajamento"].values[0])
        st.metric("Contas Engajadas", formatar_numero(engajamento_atual), f"{crescimento:.1f}%")
    else:
        st.metric("Contas Engajadas", formatar_numero(engajamento_atual), "")

with col4:
    taxa_engaj = float(df_filtrado["Taxa de Engajamento"].values[0])
    st.metric("Taxa de Engajamento", f"{taxa_engaj:.2f}%")

with col5:
    visualizacoes_atual = int(df_filtrado["Visualizações"].values[0])
    st.metric("Visualizações", formatar_numero(visualizacoes_atual))

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
                  "Taxa de Engajamento", "Interações", "Curtidas", "Comentários", "Visualizações"]
st.dataframe(df[colunas_exibir], use_container_width=True)

# Rodapé
st.divider()
st.markdown("Desenvolvido por Eduardo 🚀 | Última atualização: Março 2025")
