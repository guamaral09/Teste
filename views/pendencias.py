import streamlit as st
import pandas as pd
import os
from datetime import datetime, timedelta

CAMINHO_ARQUIVO = "dados/pendencias.csv"

def carregar_pendencias():
    if os.path.exists(CAMINHO_ARQUIVO):
        return pd.read_csv(CAMINHO_ARQUIVO, encoding="utf-8")
    else:
        return pd.DataFrame(columns=["Tarefa", "Prazo", "Status", "Processo"])

def salvar_pendencias(df):
    # Garante que o diretório "dados" existe antes de salvar
    os.makedirs(os.path.dirname(CAMINHO_ARQUIVO), exist_ok=True)
    df.to_csv(CAMINHO_ARQUIVO, index=False, encoding="utf-8")

def controle_pendencias():
    st.title("✅ Controle de Pendências")
    df = carregar_pendencias()

    with st.form("nova_pendencia"):
        st.subheader("Adicionar Nova Pendência")
        tarefa = st.text_input("Tarefa")
        prazo = st.date_input("Prazo")
        status = st.selectbox("Status", ["Pendente", "Concluído"])
        processo = st.text_input("Processo (opcional)")
        submitted = st.form_submit_button("Adicionar")

        if submitted and tarefa:
            nova_linha = {
                "Tarefa": tarefa,
                "Prazo": prazo.strftime("%Y-%m-%d"),  # Armazena em formato ISO
                "Status": status,
                "Processo": processo
            }
            df = pd.concat([df, pd.DataFrame([nova_linha])], ignore_index=True)
            salvar_pendencias(df)
            st.success("Pendência adicionada com sucesso!")
            st.rerun()

    st.subheader("Pendências Atuais")
    if not df.empty:
        st.dataframe(df, use_container_width=True)
    else:
        st.info("Nenhuma pendência cadastrada.")

def obter_pendencias_da_semana():
    df = carregar_pendencias()
    if "Prazo" not in df.columns:
        return pd.DataFrame(columns=["Tarefa", "Prazo", "Status", "Processo"])
    df["Prazo"] = pd.to_datetime(df["Prazo"], errors="coerce")
    hoje = datetime.today()
    fim_semana = hoje + timedelta(days=7)
    semana = df[(df["Prazo"] >= hoje) & (df["Prazo"] <= fim_semana)]
    return semana

def obter_pendencias_semana_e_atrasadas():
    df = carregar_pendencias()
    if "Prazo" not in df.columns:
        vazio = pd.DataFrame(columns=["Tarefa", "Prazo", "Status", "Processo"])
        return vazio, vazio

    df["Prazo"] = pd.to_datetime(df["Prazo"], errors="coerce")
    hoje = datetime.today()
    fim_semana = hoje + timedelta(days=7)

    df_filtrado = df[df["Status"].str.lower() != "concluído"]
    pendencias_semana = df_filtrado[(df_filtrado["Prazo"] >= hoje) & (df_filtrado["Prazo"] <= fim_semana)]
    pendencias_atrasadas = df_filtrado[df_filtrado["Prazo"] < hoje]

    return pendencias_semana, pendencias_atrasadas
