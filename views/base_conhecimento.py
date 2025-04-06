# views/base_conhecimento.py

import streamlit as st
import pandas as pd
from datetime import datetime

def base_conhecimento():
    st.subheader("📚 Base de Conhecimento")

    arquivo = "base_conhecimento.csv"

    # Tenta carregar base existente ou cria uma nova
    try:
        df = pd.read_csv(arquivo)
    except FileNotFoundError:
        df = pd.DataFrame(columns=["Título", "Descrição", "Data de Inclusão"])

    # Formulário para novo conteúdo
    with st.form("Nova Entrada"):
        titulo = st.text_input("Título")
        descricao = st.text_area("Descrição")
        enviado = st.form_submit_button("Adicionar")

        if enviado and titulo and descricao:
            nova_entrada = pd.DataFrame([{
                "Título": titulo,
                "Descrição": descricao,
                "Data de Inclusão": datetime.today().strftime("%Y-%m-%d %H:%M")
            }])
            df = pd.concat([df, nova_entrada], ignore_index=True)
            df.to_csv(arquivo, index=False)
            st.success("Informação adicionada com sucesso!")

    # Exibe a base
    if not df.empty:
        st.markdown("### 📖 Conteúdos Cadastrados")
        st.dataframe(df.sort_values(by="Data de Inclusão", ascending=False), use_container_width=True)
    else:
        st.info("Ainda não há registros na base de conhecimento.")
