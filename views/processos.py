# views/processos.py

import streamlit as st
import pandas as pd
import os

PROCESSOS_CSV = "processos.csv"

def carregar_processos():
    """Carrega os processos do arquivo CSV."""
    if not os.path.exists(PROCESSOS_CSV):
        return pd.DataFrame(columns=["Número do Processo", "Cliente", "Status", "Última Atualização"])
    
    try:
        return pd.read_csv(PROCESSOS_CSV, parse_dates=["Última Atualização"], dayfirst=True, encoding="utf-8")
    except Exception as e:
        st.error(f"Erro ao carregar processos: {e}")
        return pd.DataFrame(columns=["Número do Processo", "Cliente", "Status", "Última Atualização"])

def salvar_processos(df):
    """Salva o DataFrame atualizado no arquivo CSV."""
    try:
        df.to_csv(PROCESSOS_CSV, index=False, encoding="utf-8")
        st.success("✅ Processos atualizados com sucesso!")
    except Exception as e:
        st.error(f"Erro ao salvar processos: {e}")

def controle_processos():
    """Interface do Controle de Processos."""
    st.title("📋 Controle de Processos - Berggren Marcas e Patentes")

    # Carregar processos existentes
    df_processos = carregar_processos()

    # Formulário para adicionar novo processo
    with st.form("novo_processo_form"):
        numero_processo = st.text_input("Número do Processo", placeholder="Ex: BR102023000001-0")
        cliente = st.text_input("Nome do Cliente", placeholder="Nome do cliente")
        status = st.selectbox("Status", ["Em andamento", "Concluído", "Arquivado", "Suspenso"])
        ultima_atualizacao = st.date_input("Última Atualização")
        submit = st.form_submit_button("Adicionar Processo")
    
    if submit:
        if not numero_processo or not cliente:
            st.error("⚠️ Preencha todos os campos obrigatórios!")
        else:
            novo_processo = pd.DataFrame([{
                "Número do Processo": numero_processo,
                "Cliente": cliente,
                "Status": status,
                "Última Atualização": ultima_atualizacao
            }])
            df_processos = pd.concat([df_processos, novo_processo], ignore_index=True)
            salvar_processos(df_processos)
            st.experimental_rerun()  # Atualiza a página

    # Exibir processos existentes
    st.subheader("📑 Processos Cadastrados")
    if df_processos.empty:
        st.info("Nenhum processo cadastrado.")
    else:
        df_processos = df_processos.sort_values(by="Última Atualização", ascending=False)
        df_processos["Última Atualização"] = df_processos["Última Atualização"].dt.strftime("%d/%m/%Y")
        st.dataframe(df_processos)

    # Permitir exclusão de processos
    st.subheader("❌ Remover Processos")
    if not df_processos.empty:
        processo_para_excluir = st.selectbox("Selecione o processo para remover:", df_processos["Número do Processo"].tolist())
        if st.button("Remover"):
            df_processos = df_processos[df_processos["Número do Processo"] != processo_para_excluir]
            salvar_processos(df_processos)
            st.experimental_rerun()  # Atualiza a página
