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

# Cálculos cardíacos
def calcular_parametros(septo, parede, ddve, dsve, vol_atrio, asc):
    # Massa do VE (g)
    massa_ve = 0.8 * (1.04 * ((ddve + septo + parede) ** 3 - ddve ** 3)) + 0.6
    # IMVE (g/m²)
    imve = massa_ve / asc if asc > 0 else 0
    # ERP
    erp = (2 * parede) / ddve if ddve > 0 else 0
    # VAEi (mL/m²)
    vaei = vol_atrio / asc if asc > 0 else 0
    # FE Teichholz
    fe = ((ddve ** 3 - dsve ** 3) / ddve ** 3) * 100 if ddve > 0 else 0

    return massa_ve, imve, erp, vaei, fe

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
        altura = st.number_input("Altura (m)", min_value=0.0, format="%.2f")
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

        # Cálculos cardíacos
        massa_ve, imve, erp, vaei, fe = calcular_parametros(
            septo, parede_post, diam_diast, diam_sist, vol_atrio_esq, asc
        )

        st.subheader("Cálculos Cardíacos")
        st.write(f"Massa do VE: **{massa_ve:.2f} g**")
        st.write(f"Índice de Massa do VE (IMVE): **{imve:.2f} g/m²**")
        st.write(f"Espessura Relativa da Parede (ERP): **{erp:.2f}**")
        st.write(f"Volume do Átrio Esquerdo indexado (VAEi): **{vaei:.2f} mL/m²**")
        st.write(f"Fração de Ejeção (Teichholz): **{fe:.1f}%**")

        st.info("Descrição técnica e conclusão serão implementadas na próxima etapa.")
        st.write("---")
        st.write("👨‍⚕️ Desenvolvido para uso médico por ecocardiografistas.")

# Execução do app
if "logado" not in st.session_state:
    st.session_state["logado"] = False

if not st.session_state["logado"]:
    login()
else:
    formulario()
