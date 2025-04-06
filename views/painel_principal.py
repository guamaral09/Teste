import streamlit as st
from views.pendencias import obter_pendencias_semana_e_atrasadas
from views.financeiro import obter_parcelas_da_semana, obter_parcelas_em_atraso

def painel_principal():
    st.title("📊 Painel Principal")

    # Seção 1: Pendências da Semana e Atrasadas
    st.header("📌 Pendências da Semana")
    pendencias_semana, pendencias_atrasadas = obter_pendencias_semana_e_atrasadas()

    if not pendencias_semana.empty:
        for _, row in pendencias_semana.iterrows():
            st.write(f"🔸 **{row['Tarefa']}** (prazo: {row['Prazo'].strftime('%d/%m/%Y')}) — Processo: {row['Processo']}")
    else:
        st.success("Sem pendências para esta semana! ✅")

    st.header("⚠️ Pendências em Atraso")
    if not pendencias_atrasadas.empty:
        for _, row in pendencias_atrasadas.iterrows():
            st.write(f"❗ **{row['Tarefa']}** (vencida em: {row['Prazo'].strftime('%d/%m/%Y')}) — Processo: {row['Processo']}")
    else:
        st.success("Sem pendências em atraso! 🎉")

    # Seção 2: Parcelas da Semana
    st.header("📅 Parcelas a Receber nesta Semana")
    parcelas_semana = obter_parcelas_da_semana()

    if not parcelas_semana.empty:
        for _, row in parcelas_semana.iterrows():
            st.write(f"💵 **{row['Cliente']}** — {row['Serviço']} — Vencimento: {row['Vencimento']}")
    else:
        st.success("Sem parcelas a vencer nesta semana! ✅")

    # Seção 3: Parcelas em Atraso
    st.header("🚨 Parcelas em Atraso")
    parcelas_atrasadas = obter_parcelas_em_atraso()

    if not parcelas_atrasadas.empty:
        for _, row in parcelas_atrasadas.iterrows():
            st.write(f"❗ **{row['Cliente']}** — {row['Serviço']} — Vencimento: {row['Vencimento']}")
    else:
        st.success("Sem parcelas em atraso! 🎉")
