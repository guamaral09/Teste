# views/documentos.py

import streamlit as st
import os

def documentos():
    st.subheader("📁 Gestão de Documentos")

    # Diretório onde os documentos serão armazenados
    pasta_documentos = "documentos"

    # Criar diretório se não existir
    if not os.path.exists(pasta_documentos):
        os.makedirs(pasta_documentos)

    # Upload de documentos
    st.markdown("### 📤 Upload de Documentos")
    uploaded_file = st.file_uploader("Selecione um arquivo para enviar", type=["pdf", "docx", "xlsx", "png", "jpg", "jpeg"])

    if uploaded_file:
        caminho_arquivo = os.path.join(pasta_documentos, uploaded_file.name)
        with open(caminho_arquivo, "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.success(f"Arquivo '{uploaded_file.name}' salvo com sucesso!")

    # Listar documentos disponíveis
    st.markdown("### 📜 Documentos Disponíveis")
    arquivos = os.listdir(pasta_documentos)

    if arquivos:
        for arquivo in arquivos:
            caminho_arquivo = os.path.join(pasta_documentos, arquivo)
            with open(caminho_arquivo, "rb") as f:
                botao_download = st.download_button(label=f"📄 {arquivo}", data=f, file_name=arquivo)
    else:
        st.info("Nenhum documento disponível no momento.")
