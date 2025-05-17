import streamlit as st
import math

# ----- Funções auxiliares -----

def calcular_asc(peso, altura_cm):
    altura_m = altura_cm * 100  # converter cm para metros
    return round(0.007184 * (altura_m ** 0.725) * (peso ** 0.425), 2)

def calcular_massa_ve(septo_mm, parede_mm, ddve_mm):
    # Converter mm para cm
    septo = septo_mm / 10
    parede = parede_mm / 10
    ddve = ddve_mm / 10
    return round(0.8 * (1.04 * (((ddve + septo + parede)**3) - ddve**3)) + 0.6, 1)

def calcular_imve(massa_ve, asc):
    return round(massa_ve / asc, 1) if asc > 0 else 0.0

def calcular_erp(septo_mm, parede_mm, ddve_mm):
    # Converter mm para cm
    septo = septo_mm / 10
    parede = parede_mm / 10
    ddve = ddve_mm / 10
    return round((2 * parede) / ddve, 2) if ddve > 0 else 0.0

def calcular_vaei(volume_ae, asc):
    return round(volume_ae / asc, 1) if asc > 0 else 0.0

def calcular_fe_teichholz(ddve_mm, dsve_mm):
    if ddve_mm == 0:
        return 0.0
    return round(((ddve_mm**3 - dsve_mm**3) / ddve_mm**3) * 100, 1)

# ----- App Streamlit -----

st.set_page_config(page_title="Laudo de Ecocardiograma", layout="centered")
st.title("🫀 Laudo Ecocardiograma")

# --- Login Simples ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.subheader("Login")
    username = st.text_input("Usuário")
    password = st.text_input("Senha", type="password")
    if st.button("Entrar"):
        if username == "admin" and password == "admin":
            st.session_state.logged_in = True
        else:
            st.error("Usuário ou senha incorretos.")
    st.stop()

# --- Formulário do Paciente ---
st.header("Informações do Paciente")
nome = st.text_input("Nome do paciente")
peso = st.number_input("Peso (kg)", min_value=0.0, format="%.2f")
altura = st.number_input("Altura (m)", min_value=0.0, format="%.2f")
genero = st.selectbox("Gênero", ["Masculino", "Feminino"])

st.header("Medidas (em milímetros)")
aorta = st.number_input("Aorta", min_value=0.0, format="%.2f")
ae = st.number_input("Átrio Esquerdo", min_value=0.0, format="%.2f")
septo = st.number_input("Septo Interventricular", min_value=0.0, format="%.2f")
parede = st.number_input("Parede Posterior", min_value=0.0, format="%.2f")
ddve = st.number_input("Diâmetro Diastólico do VE", min_value=0.0, format="%.2f")
dsve = st.number_input("Diâmetro Sistólico do VE", min_value=0.0, format="%.2f")
volume_ae = st.number_input("Volume do Átrio Esquerdo (mL)", min_value=0.0, format="%.2f")

if st.button("Gerar Laudo"):
    asc = calcular_asc(peso, altura)
    massa_ve = calcular_massa_ve(septo, parede, ddve)
    imve = calcular_imve(massa_ve, asc)
    erp = calcular_erp(septo, parede, ddve)
    vaei = calcular_vaei(volume_ae, asc)
    fe = calcular_fe_teichholz(ddve, dsve)

    st.subheader("📐 Resultados Calculados")
    st.write(f"**Área de Superfície Corporal (ASC)**: {asc} m²")
    st.write(f"**Massa do VE**: {massa_ve} g")
    st.write(f"**Índice de Massa do VE (IMVE)**: {imve} g/m²")
    st.write(f"**Espessura Relativa da Parede (ERP)**: {erp}")
    st.write(f"**Volume do AE indexado (VAEi)**: {vaei} mL/m²")
    st.write(f"**Fração de Ejeção (Teichholz)**: {fe} %")

    st.success("Cálculos realizados com sucesso! Geração de laudo em breve.")

