# views/orcamento.py

import streamlit as st
import os
from fpdf import FPDF

def simulador_orcamento():
    st.subheader("🧾 Simulador de Orçamento")

    # Entrada de dados
    qtd_classes = st.number_input("Quantidade de Classes", min_value=1, value=1, step=1)
    porte_empresa = st.selectbox("Porte da Empresa", ["MEI", "Microempresa", "Empresa de Pequeno Porte", "Demais"])
    
    honorarios = 1200.00  # Exemplo de valor fixo de honorários
    taxa_inpi = 142.00 if porte_empresa in ["MEI", "Microempresa", "Empresa de Pequeno Porte"] else 355.00
    taxa_inpi_total = taxa_inpi * qtd_classes

    valor_total = honorarios + taxa_inpi_total

    # Exibe valores calculados
    st.markdown(f"**Honorários:** R$ {honorarios:.2f}")
    st.markdown(f"**Taxas INPI estimadas:** R$ {taxa_inpi_total:.2f}")
    st.markdown(f"**Valor total estimado:** R$ {valor_total:.2f}")

    # Gerar orçamento em PDF
    if st.button("📄 Gerar Orçamento PDF"):
        nome_arquivo = gerar_pdf_orcamento(valor_total, honorarios, taxa_inpi_total, qtd_classes, porte_empresa)
        with open(nome_arquivo, "rb") as f:
            st.download_button(label="📥 Baixar Orçamento", data=f, file_name=nome_arquivo, mime="application/pdf")

def gerar_pdf_orcamento(valor_total, honorarios, taxa_inpi, qtd_classes, porte_empresa):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    if os.path.exists("logo_berggren.png"):
        pdf.image("logo_berggren.png", x=10, y=8, w=33)
    
    pdf.ln(30)
    pdf.cell(200, 10, txt="Orçamento - Registro de Marca", ln=True, align="C")
    pdf.ln(10)

    pdf.cell(200, 10, txt=f"Número de classes: {qtd_classes}", ln=True)
    pdf.cell(200, 10, txt=f"Porte da empresa: {porte_empresa}", ln=True)
    pdf.cell(200, 10, txt=f"Honorários: R$ {honorarios:.2f}", ln=True)
    pdf.cell(200, 10, txt=f"Taxas INPI estimadas: R$ {taxa_inpi:.2f}", ln=True)
    pdf.ln(5)
    pdf.cell(200, 10, txt=f"Valor total estimado: R$ {valor_total:.2f}", ln=True)

    pdf.ln(10)
    pdf.set_font("Arial", size=10)
    pdf.multi_cell(0, 10, txt="Este orçamento é uma estimativa com base nas informações fornecidas e está sujeito a alterações conforme análise específica do caso e eventual atualização das taxas oficiais.")

    nome_arquivo = "orcamento_berggren.pdf"
    pdf.output(nome_arquivo)
    return nome_arquivo
