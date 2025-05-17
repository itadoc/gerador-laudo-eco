import streamlit as st

# Usuários e senhas simples
USERS = {
    "medico1": "senha123",
    "ecocardio": "eco2025"
}

# Função para calcular a Área de Superfície Corporal (Dubois)
def calcular_asc(peso, altura_cm):
    altura_m = altura_cm * 100  # converte cm para metros
    asc = 0.007184 * (altura_m ** 0.725) * (peso ** 0.425)
    return asc

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

# Página principal com formulário de entrada
def formulario():
    st.title("Laudo Ecocardiograma")

    with st.form("dados_paciente"):
        st.subheader("Informações do Paciente")
        nome = st.text_input("Nome do paciente")
        peso = st.number_input("Peso (kg)", min_value=0.0, format="%.2f")
        altura = st.number_input("Altura (cm)", min_value=0.0, format="%.2f")
        genero = st.selectbox("Gênero", ["Masculino", "Feminino"])

        st.subheader("Medidas (em milímetros)")
        aorta = st.number_input("Aorta", min_value=0.0)
        atrio_esq = st.number_input("Átrio Esquerdo", min_value=0.0)
        septo = st.number_input("Septo Interventricular", min_value=0.0)
        parede_post = st.number_input("Parede Posterior", min_value=0.0)
        diam_diast = st.number_input("Diâmetro Diastólico do VE", min_value=0.0)
        diam_sist = st.number_input("Diâmetro Sistólico do VE", min_value=0.0)
        vol_atrio_esq = st.number_input("Volume do Átrio Esquerdo (mL)", min_value=0.0)

        enviado = st.form_submit_button("Calcular")

    if enviado:
        asc = calcular_asc(peso, altura)
        st.success(f"Área de Superfície Corporal (ASC): {asc:.2f} m²")

        st.info("Cálculos adicionais serão implementados na próxima etapa.")
        st.write("---")
        st.write("👨‍⚕️ Desenvolvido para uso médico por ecocardiografistas.")

# Execução do app
if "logado" not in st.session_state:
    st.session_state["logado"] = False

if not st.session_state["logado"]:
    login()
else:
    formulario()
