# Ferramenta para gerar laudo de ecocardiograma transtorácico em formato Word e compatível com Google Docs
# Requisitos: openai, python-docx, streamlit

import openai
from docx import Document
from docx.shared import Pt
import streamlit as st
import tempfile
import os
import re

# Configure sua chave da OpenAI
openai.api_key = st.secrets["OPENAI_API_KEY"]

st.title("Gerador de Laudo de Ecocardiograma Transtorácico (Word/Google Docs)")

input_text = st.text_area("Digite os achados do ecocardiograma transtorácico (relato verbal):", height=200)
altura = st.number_input("Altura do paciente (cm):", min_value=100, max_value=250, step=1)
peso = st.number_input("Peso do paciente (kg):", min_value=30.0, max_value=250.0, step=0.1)

# Função para calcular fração de ejeção pelo método de Teichholz
def calcular_teichholz(ddve, dsve):
    try:
        fe = ((ddve**3 - dsve**3) / ddve**3) * 100
        return round(fe, 1)
    except:
        return None

# Função para calcular área de superfície corporal (Du Bois)
def calcular_asc(altura_cm, peso_kg):
    try:
        asc = 0.007184 * (altura_cm ** 0.725) * (peso_kg ** 0.425)
        return round(asc, 2)
    except:
        return None

# Função para extrair medidas numéricas do texto
def extrair_medidas(texto):
    ddve = dsve = vol_ae = None
    ddve_match = re.search(r"diast[oô]lico.*?(\d{2,3})\s*mm", texto, re.IGNORECASE)
    dsve_match = re.search(r"sist[oô]lico.*?(\d{2,3})\s*mm", texto, re.IGNORECASE)
    vol_ae_match = re.search(r"volume do[\s\w]*[áa]trio esquerdo.*?(\d{2,3})\s*m[lL]", texto, re.IGNORECASE)

    if ddve_match:
        ddve = int(ddve_match.group(1))
    if dsve_match:
        dsve = int(dsve_match.group(1))
    if vol_ae_match:
        vol_ae = int(vol_ae_match.group(1))

    return ddve, dsve, vol_ae

if st.button("Gerar Laudo e Baixar Word/Google Docs"):
    if input_text.strip() == "":
        st.warning("Por favor, insira os achados do exame.")
    else:
        ddve, dsve, vol_ae = extrair_medidas(input_text)
        fe_teichholz = calcular_teichholz(ddve, dsve) if ddve and dsve else None
        asc = calcular_asc(altura, peso) if altura and peso else None
        vol_indexado = round(vol_ae / asc, 1) if vol_ae and asc else None

        # Inserir cálculos adicionais no prompt fixamente na seção de medidas
        medidas_extras = "\n\nMedidas:"  # Força início da seção Medidas no laudo
        if ddve and dsve and fe_teichholz:
            medidas_extras += f"\n- Fração de ejeção estimada pelo método de Teichholz: {fe_teichholz}% (DDVE: {ddve} mm, DSVE: {dsve} mm)"
        if vol_ae and asc and vol_indexado:
            medidas_extras += f"\n- Volume do átrio esquerdo: {vol_ae} mL, indexado por ASC ({asc} m²): {vol_indexado} mL/m²"

        prompt = f"""
Transforme o seguinte relato verbal de ecocardiograma transtorácico em um laudo médico padronizado com as seções:
1) Medidas
2) Função ventricular
3) Estruturas valvares
4) Cavidades cardíacas
5) Pericárdio
6) Conclusão
Use linguagem técnica e objetiva, como um laudo médico real.

Relato: {input_text}
{medidas_extras}
"""

        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "Você é um médico cardiologista especialista em ecocardiografia."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=900
            )

            laudo = response.choices[0].message.content

            # Criar documento Word compatível com Google Docs
            doc = Document()
            doc.add_heading("Laudo de Ecocardiograma Transtorácico", level=1)

            for line in laudo.splitlines():
                if line.strip() == "":
                    doc.add_paragraph("")
                elif line.endswith(":"):
                    doc.add_heading(line.strip(), level=2)
                else:
                    p = doc.add_paragraph(line.strip())
                    p.style.font.size = Pt(11)

            # Salvar como .docx compatível com Google Docs
            with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as tmp:
                doc.save(tmp.name)
                tmp_path = tmp.name

            with open(tmp_path, "rb") as file:
                st.download_button(
                    label="📥 Baixar Laudo (Word/Google Docs)",
                    data=file,
                    file_name="laudo_ecocardiograma_transtoracico.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                )

            os.unlink(tmp_path)

        except Exception as e:
            st.error(f"Erro ao gerar laudo: {e}")
