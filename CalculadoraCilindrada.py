import streamlit as st
import sqlite3
import hashlib
import math

# Função para criar banco de dados e tabela de usuários
def criar_banco_dados():
    conn = sqlite3.connect('usuarios.db')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS usuarios (
        username TEXT PRIMARY KEY,
        password TEXT NOT NULL
    )
    ''')
    conn.commit()
    conn.close()

# Função para hash de senha
def hash_senha(senha):
    return hashlib.sha256(senha.encode()).hexdigest()

# Função para registrar usuário
def registrar_usuario(username, senha):
    conn = sqlite3.connect('usuarios.db')
    cursor = conn.cursor()
    
    try:
        hashed_senha = hash_senha(senha)
        cursor.execute('INSERT INTO usuarios (username, password) VALUES (?, ?)', 
                       (username, hashed_senha))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

# Função para verificar login
def verificar_login(username, senha):
    conn = sqlite3.connect('usuarios.db')
    cursor = conn.cursor()
    
    hashed_senha = hash_senha(senha)
    cursor.execute('SELECT * FROM usuarios WHERE username = ? AND password = ?', 
                   (username, hashed_senha))
    
    usuario = cursor.fetchone()
    conn.close()
    
    return usuario is not None

# Funções de cálculo (mantidas do código anterior)
def calcular_cilindrada(diametro_pistao, curso_virabrequim, num_cilindros):
    raio_pistao = diametro_pistao / 2
    volume_cilindro = math.pi * (raio_pistao ** 2) * curso_virabrequim
    cilindrada_total = (volume_cilindro * num_cilindros) / 1000
    return round(cilindrada_total, 2)

def calcular_rl(diametro_pistao, curso_virabrequim):
    raio_pistao = diametro_pistao / 2
    rl = raio_pistao / curso_virabrequim
    return round(rl, 3)

def classificar_motor_por_rl(rl):
    if rl < 0.5:
        return "Motor Supercurso (Stroke)"
    elif 0.5 <= rl < 0.8:
        return "Motor Curso Médio"
    else:
        return "Motor Curto (Oversquare)"

# Inicializar banco de dados
criar_banco_dados()

# Configuração da página do Streamlit
st.set_page_config(page_title="Calculadora de Cilindrada", page_icon="🚗", layout="centered")

# Função para página de login
def pagina_login():
    st.title("🚗 Login - Calculadora de Motor")
    
    # Abas de Login e Registro
    tab1, tab2 = st.tabs(["Login", "Registrar"])
    
    with tab1:
        username = st.text_input("Usuário", key="login_username")
        senha = st.text_input("Senha", type="password", key="login_senha")
        
        if st.button("Entrar"):
            if verificar_login(username, senha):
                st.session_state['logado'] = True
                st.session_state['username'] = username
                st.rerun()
            else:
                st.error("Usuário ou senha incorretos")
    
    with tab2:
        novo_username = st.text_input("Novo Usuário", key="registro_username")
        nova_senha = st.text_input("Nova Senha", type="password", key="registro_senha")
        confirmar_senha = st.text_input("Confirmar Senha", type="password", key="registro_confirmar")
        
        if st.button("Registrar"):
            if nova_senha == confirmar_senha:
                if registrar_usuario(novo_username, nova_senha):
                    st.success("Usuário registrado com sucesso!")
                else:
                    st.error("Usuário já existe")
            else:
                st.error("Senhas não coincidem")

# Função para página principal
def pagina_principal():
    st.title("🚗 Calculadora de Cilindrada de Motor")
    st.markdown(f"Bem-vindo, {st.session_state['username']}!")
    
    # Botão de logout
    if st.sidebar.button("Sair"):
        st.session_state['logado'] = False
        st.session_state['username'] = None
        st.rerun()
    
    # Resto do código de cálculo (mantido igual ao anterior)
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

# Lógica principal
def main():
    # Inicializar estado de login se não existir
    if 'logado' not in st.session_state:
        st.session_state['logado'] = False
    
    # Verificar estado de login
    if not st.session_state['logado']:
        pagina_login()
    else:
        pagina_principal()

# Executar aplicativo
if __name__ == "__main__":
    main()
