import streamlit as st

# Importações das views
from views.painel_principal import painel_principal
from views.tarefas import exibir_tarefas
from views.base_conhecimento import base_conhecimento
from views.relatorios import relatorios
from views.orcamento import simulador_orcamento
from views.parecer import gerar_parecer
from views.documentos import documentos  # <-- Nova view adicionada
from views.pendencias import controle_pendencias
from views.financeiro import exibir_financeiro
from views.processos import controle_processos

def main():
    st.set_page_config(page_title="Sistema Berggren", layout="wide")

    st.sidebar.title("📂 Menu de Navegação")

    # Categorias principais
    categoria = st.sidebar.selectbox("Escolha uma categoria:", [
        "📊 Painel",
        "🛠️ Ferramentas",
        "📋 Controle"
    ])

    submenu = None

    # Submenus conforme a categoria selecionada
    if categoria == "📊 Painel":
        submenu = st.sidebar.radio("Painel", [
            "📊 Painel Principal",
            "📌 Tarefas / Roadmap"
        ])
    elif categoria == "🛠️ Ferramentas":
        submenu = st.sidebar.radio("Ferramentas", [
            "📚 Base de Conhecimento",
            "📊 Relatórios",
            "🧾 Simulador de Orçamento",
            "📄 Gerador de Parecer",
            "📁 Gestão de Documentos"  # <-- Adicionado aqui
        ])
    elif categoria == "📋 Controle":
        submenu = st.sidebar.radio("Controle", [
            "📌 Controle de Pendências",
            "💰 Controle Financeiro",
            "📋 Controle de Processos"
        ])

    # Execução conforme submenu
    if submenu == "📊 Painel Principal":
        painel_principal()
    elif submenu == "📌 Tarefas / Roadmap":
        exibir_tarefas()
    elif submenu == "📚 Base de Conhecimento":
        base_conhecimento()
    elif submenu == "📊 Relatórios":
        relatorios()
    elif submenu == "🧾 Simulador de Orçamento":
        simulador_orcamento()
    elif submenu == "📄 Gerador de Parecer":
        gerar_parecer()
    elif submenu == "📁 Gestão de Documentos":
        documentos()
    elif submenu == "📌 Controle de Pendências":
        controle_pendencias()
    elif submenu == "💰 Controle Financeiro":
        exibir_financeiro()
    elif submenu == "📋 Controle de Processos":
        controle_processos()

# Execução do sistema
if __name__ == "__main__":
    main()
