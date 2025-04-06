# views/agenda.py

import streamlit as st
import pandas as pd
from datetime import datetime

def agenda():
    st.subheader("📆 Agendamentos")

    arquivo = "agendamentos.csv"

    # Carrega ou cria DataFrame
    try:
        df = pd.read_csv(arquivo, parse_dates=["Data"])
    except FileNotFoundError:
        df = pd.DataFrame(columns=["Data", "Hora", "Compromisso"])

    # Formulário de novo agendamento
    with st.form("Novo Agendamento"):
        data = st.date_input("Data", value=datetime.today())
        hora = st.time_input("Hora")
        compromisso = st.text_input("Compromisso")
        submitted = st.form_submit_button("Adicionar")
        if submitted and compromisso:
            novo_agendamento = pd.DataFrame([{
                "Data": data,
                "Hora": hora.strftime("%H:%M"),
                "Compromisso": compromisso
            }])
            df = pd.concat([df, novo_agendamento], ignore_index=True)
            df.to_csv(arquivo, index=False)
            st.success("Agendamento salvo com sucesso!")

    # Exibe agendamentos futuros
    st.markdown("### 📅 Próximos Agendamentos")
    hoje = pd.to_datetime(datetime.today().date())
    df["Data"] = pd.to_datetime(df["Data"])
    futuros = df[df["Data"] >= hoje].sort_values(by=["Data", "Hora"])

    if not futuros.empty:
        st.dataframe(futuros, use_container_width=True)
    else:
        st.info("Nenhum agendamento futuro encontrado.")
