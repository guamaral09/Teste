# views/parecer.py

import streamlit as st
import csv
from datetime import datetime

def gerar_parecer():
    st.title("📄 Gerador de Parecer - Berggren Marcas e Patentes")
    
    # Formulário para entrada de dados
    with st.form("parecer_form"):
        nome = st.text_input("Nome do Cliente", placeholder="Digite o nome do cliente")
        classe = st.text_input("Classe da Marca", placeholder="Digite a classe da marca")
        parecer = st.selectbox("Parecer", ["Favorável", "Desfavorável"])
        justificativa = st.text_area("Justificativa", placeholder="Explique o motivo do parecer")
        cidade = st.text_input("Cidade", placeholder="Digite a cidade do cliente")
        
        submitted = st.form_submit_button("Gerar Parecer")
    
    if submitted:
        if not nome or not classe or not justificativa or not cidade:
            st.error("⚠️ Todos os campos são obrigatórios!")
            return

        # Formatar data atual
        data_atual = datetime.today().strftime("%d/%m/%Y")

        # Salvar parecer no histórico CSV
        try:
            with open("historico_pareceres.csv", mode="a", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerow([data_atual, nome, classe, parecer, justificativa, cidade])
            st.success("✅ Parecer salvo com sucesso!")
        except Exception as e:
            st.error(f"Erro ao salvar parecer: {e}")

        # Exibir resultado
        st.subheader("📜 Parecer Gerado")
        st.write(f"**Data:** {data_atual}")
        st.write(f"**Cliente:** {nome}")
        st.write(f"**Classe:** {classe}")
        st.write(f"**Parecer:** {parecer}")
        st.write(f"**Justificativa:** {justificativa}")
        st.write(f"**Cidade:** {cidade}")
