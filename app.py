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
    # Correção com fórmula completa de Teichholz (volumes)
    ddve = ddve_mm / 10
    dsve = dsve_mm / 10
    if ddve == 0 or dsve == 0:
        return 0.0
    edv = (7.0 / (2.4 + ddve)) * ddve**3
    esv = (7.0 / (2.4 + dsve)) * dsve**3
    fe = ((edv - esv) / edv) * 100
    return round(fe, 2)

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
from docx import Document
from docx.shared import Pt

# Geração do texto do laudo com base nos dados
if st.session_state.logged_in and 'bsa' in locals():
    st.subheader("Texto do Laudo")

    laudo_texto = f"""
Laudo Ecocardiograma

Ventrículo esquerdo: cavidade com dimensões normais, paredes com espessura normal, ausência de alteração da contratilidade segmentar, função sistólica e diastólica normal.

Átrio esquerdo: dimensões normais, volume indexado normal.

Ventrículo direito e átrio direito: cavidades com dimensões normais, função sistólica normal.

Valva aórtica: folhetos com espessura e mobilidade normais, abertura valvar preservada, ausência de refluxo aórtico.

Valva mitral: folhetos com espessura e mobilidade normais, abertura valvar preservada, refluxo fisiológico.

Valva tricúspide: folhetos com espessura e mobilidade normais, refluxo mínimo, fisiológico.

Valva pulmonar: folhetos com espessura e mobilidade normais, refluxo mínimo, fisiológico.

Pericárdio: ausência de derrame pericárdico.

Conclusão: Ecocardiograma transtorácico normal.
"""

    st.text_area("Texto do Laudo", laudo_texto, height=400)

    # Criação de arquivo DOCX
    document = Document()
    style = document.styles['Normal']
    font = style.font
    font.name = 'Calibri'
    font.size = Pt(12)

    document.add_heading('Laudo Ecocardiograma', level=1)
    document.add_paragraph(f"Paciente: {nome}")
    document.add_paragraph(f"Peso: {peso} kg")
    document.add_paragraph(f"Altura: {altura} cm")
    document.add_paragraph(f"Gênero: {genero}")
    document.add_paragraph(f"Área de Superfície Corporal (ASC): {bsa:.2f} m²")
    document.add_paragraph("")

    for linha in laudo_texto.strip().split('\n\n'):
        document.add_paragraph(linha.strip())

    # Salvar o arquivo temporariamente
    docx_path = "/tmp/laudo_ecocardiograma.docx"
    document.save(docx_path)

    with open(docx_path, "rb") as file:
        st.download_button(
            label="📄 Baixar Laudo em DOCX",
            data=file,
            file_name="laudo_ecocardiograma.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
