import streamlit as st

def exibir_tarefas():
    st.title("📌 Tarefas / Roadmap")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.header("✅ Concluídas")
        st.markdown("- Integração com painel financeiro")
        st.markdown("- Layout da aba Painel Principal")
        st.markdown("- Exibição de pendências da semana")

    with col2:
        st.header("🔧 Em andamento")
        st.markdown("- Otimização de mensagens de erro")
        st.markdown("- Ajustes nos filtros de vencimento")

    with col3:
        st.header("📝 A fazer")
        st.markdown("- Notificações por e-mail")
        st.markdown("- Upload de documentos em PDF")

    with col4:
        st.header("💡 Ideias futuras")
        st.markdown("- Dashboard de indicadores")
        st.markdown("- Gráficos financeiros mensais")
