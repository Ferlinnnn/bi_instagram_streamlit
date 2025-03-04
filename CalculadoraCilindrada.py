import streamlit as st
import math

def calcular_cilindrada(diametro_pistao, curso_virabrequim, num_cilindros):
    """
    Calcula a cilindrada total do motor
    
    Parâmetros:
    - diametro_pistao: Diâmetro do pistão em milímetros
    - curso_virabrequim: Curso do virabrequim em milímetros
    - num_cilindros: Número de cilindros do motor
    
    Retorna:
    - Cilindrada total em centímetros cúbicos (cc)
    """
    # Fórmula da cilindrada: (π * (diâmetro/2)² * curso * número de cilindros) / 1000
    raio_pistao = diametro_pistao / 2
    volume_cilindro = math.pi * (raio_pistao ** 2) * curso_virabrequim
    cilindrada_total = (volume_cilindro * num_cilindros) / 1000
    
    return round(cilindrada_total, 2)

def calcular_rl(diametro_pistao, curso_virabrequim):
    """
    Calcula a relação Raio/Curso (R/L)
    
    Parâmetros:
    - diametro_pistao: Diâmetro do pistão em milímetros
    - curso_virabrequim: Curso do virabrequim em milímetros
    
    Retorna:
    - Relação R/L
    """
    raio_pistao = diametro_pistao / 2
    rl = raio_pistao / curso_virabrequim
    return round(rl, 3)

def classificar_motor_por_rl(rl):
    """
    Classifica o tipo de motor baseado na relação R/L
    
    Parâmetros:
    - rl: Relação Raio/Curso
    
    Retorna:
    - Classificação do motor
    """
    if rl < 0.5:
        return "Motor Supercurso (Stroke)"
    elif 0.5 <= rl < 0.8:
        return "Motor Curso Médio"
    else:
        return "Motor Curto (Oversquare)"

# Configuração da página do Streamlit
st.set_page_config(
    page_title="Calculadora de Cilindrada",
    page_icon="🚗",
    layout="centered"
)

# Título do aplicativo
st.title("🚗 Calculadora de Cilindrada de Motor")
st.markdown("Calcule a cilindrada total do seu motor")

# Entrada de dados
col1, col2, col3 = st.columns(3)

with col1:
    diametro_pistao = st.number_input(
        "Diâmetro do Pistão (mm)", 
        min_value=1.0, 
        max_value=200.0, 
        value=80.0, 
        step=0.1
    )

with col2:
    curso_virabrequim = st.number_input(
        "Curso do Virabrequim (mm)", 
        min_value=1.0, 
        max_value=200.0, 
        value=70.0, 
        step=0.1
    )

with col3:
    num_cilindros = st.number_input(
        "Número de Cilindros", 
        min_value=1, 
        max_value=16, 
        value=4, 
        step=1
    )

# Botão para calcular
if st.button("Calcular Cilindrada"):
    # Realizar cálculo
    cilindrada = calcular_cilindrada(diametro_pistao, curso_virabrequim, num_cilindros)
    
    # Calcular R/L
    rl = calcular_rl(diametro_pistao, curso_virabrequim)
    classificacao_motor = classificar_motor_por_rl(rl)
    
    # Exibir resultados
    st.subheader("Resultados")
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric(label="Cilindrada Total", value=f"{cilindrada} cc")
    
    with col2:
        st.metric(label="Relação R/L", value=rl)
    
    # Classificação do motor
    st.markdown(f"**Tipo de Motor:** {classificacao_motor}")
    
    # Informações adicionais
    st.markdown("### Detalhes do Cálculo")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"**Diâmetro do Pistão:** {diametro_pistao} mm")
    
    with col2:
        st.markdown(f"**Curso do Virabrequim:** {curso_virabrequim} mm")
    
    with col3:
        st.markdown(f"**Número de Cilindros:** {num_cilindros}")
    
    with col4:
        st.markdown(f"**Relação R/L:** {rl}")

# Rodapé com informações
st.markdown("---")
st.markdown("""
### Sobre o Cálculo de Cilindrada e Relação R/L

**Cilindrada:**
- Volume do Cilindro = π * (Raio do Pistão)² * Curso do Virabrequim
- Cilindrada Total = Volume do Cilindro * Número de Cilindros

**Relação R/L (Raio/Curso):**
- R/L < 0.5: Motor Supercurso (Stroke)
- 0.5 ≤ R/L < 0.8: Motor Curso Médio
- R/L ≥ 0.8: Motor Curto (Oversquare)

**Significado:**
- Influencia características como torque, rotação máxima e eficiência
- Afeta o desempenho e comportamento do motor
""")

st.markdown("Desenvolvido por Ferlin & Jão sem Dedo| Cálculos Baseados em Engenharia mecânica") 
