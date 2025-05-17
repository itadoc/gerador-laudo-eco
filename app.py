import streamlit as st

# Usuários e senhas simples (em produção use hash e banco de dados)
USERS = {
    "medico1": "senha123",
    "ecocardio": "eco2025"
}

# Função para calcular área de superfície corporal (Dubois)
def calcular_asc(peso, altura):
    return 0.007184 * (peso ** 0.425) * (altura ** 0.725)

# Autenticação simples
def autenticar(usuario, senha):
    return USERS.get(usuario) == senha

# Sessão de login
def login():
    st.title("Login - Sistema de Laudo Ecocardiográfico")
    usuario = st.text_input("Usuário")
    senha = st.text_input("Senha", type="password")
    if st.button("Entrar"):
        if autenticar(usuario, senha):
            st.session_state["logado"] = True
            st.session_state["usuario"] = usuario
        else:
            st.error("Usuário ou senha inválidos")

# Página principal com formulário
def formulario():
    st.title("Laudo Ecocardiograma")

    with st.form("dados_paciente"):
        st.subheader("Informações do Paciente")
        nome = st.text_input("Nome")
        peso = st.number_input("Peso (kg)", min_value=0.0, format="%.2f")
        altura = st.number_input("Altura (cm)", min_value=0.0, format="%.2f")
        genero = st.selectbox("Gênero", ["Masculino", "Feminino"])

        st.subheader("Medidas (em milímetros)")
        aorta = st.number_input("Aorta", min_value=0.0)
        atrio_esq = st.number_input("Átrio Esquerdo", min_value=0.0)
        septo = st.number_input("Septo Interventricular", min_value=0.0)
        parede_post = st.number_input("Parede Posterior", min_value=0.0)
        diam_diast = st.number_input("Diâmetro Diastólico VE", min_value=0.0)
        diam_sist = st.number_input("Diâmetro Sistólico VE", min_value=0.0)
        vol_atrio_esq = st.number_input("Volume do Átrio Esquerdo (mL)", min_value=0.0)

        enviado = st.form_submit_button("Calcular")

    if enviado:
        altura_m = altura / 100  # converter cm para metros
        asc = calcular_asc(peso, altura_m)
        st.success(f"Área de Superfície Corporal (ASC): {asc:.2f} m²")

        # Aqui serão chamados os próximos cálculos (massa VE, FE etc.)
        st.info("Cálculos adicionais virão na próxima etapa.")

# Execução do app
if "logado" not in st.session_state:
    st.session_state["logado"] = False

if not st.session_state["logado"]:
    login()
else:
    formulario()
