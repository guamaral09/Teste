# views/relatorios.py

import streamlit as st
import pandas as pd
import os

def relatorios():
    st.subheader("📊 Relatórios")

    # Nome do arquivo de relatórios
    arquivo = "relatorios.csv"

    # Verifica se o arquivo existe e carrega os dados
    if os.path.exists(arquivo):
        df = pd.read_csv(arquivo)
    else:
        df = pd.DataFrame(columns=["Data", "Categoria", "Descrição"])

    # Formulário para adicionar um novo relatório
    with st.form("Novo Relatório"):
        data = st.date_input("Data")
        categoria = st.selectbox("Categoria", ["Financeiro", "Jurídico", "Comercial", "Operacional"])
        descricao = st.text_area("Descrição")
        enviado = st.form_submit_button("Adicionar Relatório")

        if enviado and descricao:
            nova_entrada = pd.DataFrame([{
                "Data": data.strftime("%Y-%m-%d"),
                "Categoria": categoria,
                "Descrição": descricao
            }])
            df = pd.concat([df, nova_entrada], ignore_index=True)
            df.to_csv(arquivo, index=False)
            st.success("Relatório adicionado com sucesso!")

    # Exibe os relatórios cadastrados
    if not df.empty:
        st.markdown("### 📜 Relatórios Registrados")
        st.dataframe(df.sort_values(by="Data", ascending=False), use_container_width=True)
    else:
        st.info("Nenhum relatório cadastrado no momento.")
