import streamlit as st
import pandas as pd
from datetime import datetime
import os

# Mapeamento de status
STATUS_MAP = {
    "IPAS009": "Publicação de pedido de registro para oposição (exame formal concluído)",
    "IPAS024": "Indeferimento do pedido",
    "IPAS029": "Deferimento do pedido",
    "IPAS136": "Exigência de mérito",
    "IPAS139": "Arquivamento definitivo de pedido de registro por falta de cumprimento de exigência de mérito",
    "IPAS142": "Sobrestamento do exame de mérito",
    "IPAS157": "Arquivamento definitivo de pedido de registro por falta de pagamento da concessão",
    "IPAS158": "Concessão de registro",
    "IPAS161": "Extinção de registro pela expiração do prazo de vigência",
    "IPAS304": "Extinção de registro pela caducidade",
    "IPAS395": "Exigência de pagamento",
    "IPAS423": "Notificação de oposição",
    "IPAS235": "Recurso não provido (decisão mantida)",
    "IPAS400": "Notificação de instauração de processo de nulidade a requerimento"
}

CAMINHO_CSV = "dados/processos.csv"

def carregar_processos():
    if os.path.exists(CAMINHO_CSV):
        df = pd.read_csv(CAMINHO_CSV)
    else:
        df = pd.DataFrame(columns=["Número do Processo", "Marca", "Status", "Apresentação", "Titular", "Classe", "Código", "Última Atualização"])
    return df

def salvar_processos(df):
    df.to_csv(CAMINHO_CSV, index=False)

def controle_processos():
    st.title("📋 Controle de Processos")
    df_processos = carregar_processos()

    # Formulário de novo processo (minimizado)
    with st.expander("Adicionar Novo Processo"):
        with st.form("novo_processo"):
            st.subheader("Adicionar Novo Processo")
            numero_processo = st.text_input("Número do Processo")
            marca = st.text_input("Marca")
            status_selecionado = st.selectbox("Selecione o status do processo", list(STATUS_MAP.values()))
            codigo_status = [codigo for codigo, status in STATUS_MAP.items() if status == status_selecionado][0]
            apresentacao = st.selectbox("Apresentação", ["Mista", "Nominativa", "Figurativa"])
            titular = st.text_input("Titular")
            classe = st.text_input("Classe")
            ultima_atualizacao = datetime.today().strftime("%d/%m/%Y")
            submitted = st.form_submit_button("Adicionar")

            if submitted and numero_processo:
                nova_linha = {
                    "Número do Processo": numero_processo,
                    "Marca": marca,
                    "Status": status_selecionado,
                    "Apresentação": apresentacao,
                    "Titular": titular,
                    "Classe": classe,
                    "Código": codigo_status,
                    "Última Atualização": ultima_atualizacao
                }
                df_processos = pd.concat([df_processos, pd.DataFrame([nova_linha])], ignore_index=True)
                salvar_processos(df_processos)
                st.success(f"Processo {numero_processo} adicionado com sucesso!")

    # Busca por Titular e Número do Processo
    st.subheader("Buscar Processos")
    search_titular = st.text_input("Buscar por Titular")
    search_numero = st.text_input("Buscar por Número do Processo")

    # Garantir que a coluna "Número do Processo" e "Titular" sejam tratadas como string
    df_processos["Número do Processo"] = df_processos["Número do Processo"].astype(str)
    df_processos["Titular"] = df_processos["Titular"].astype(str)

    if search_titular:
        df_processos = df_processos[df_processos["Titular"].str.contains(search_titular, case=False)]
    if search_numero:
        df_processos = df_processos[df_processos["Número do Processo"].str.contains(search_numero, case=False)]


    # Exibição dos processos cadastrados sem a coluna numérica extra
    st.subheader("Processos Cadastrados")
    if not df_processos.empty:
        # Exibe o cabeçalho
        col_header = st.columns([2, 2, 2, 2, 2, 1, 1])
        col_header[0].markdown("**Número do Processo**")
        col_header[1].markdown("**Marca**")
        col_header[2].markdown("**Status**")
        col_header[3].markdown("**Apresentação**")
        col_header[4].markdown("**Titular**")
        col_header[5].markdown("**Classe**")
        col_header[6].markdown("**Ações**")

        # Exibe a tabela de processos
        for i, row in df_processos.iterrows():
            col1, col2, col3, col4, col5, col6, col7 = st.columns([2, 2, 2, 2, 2, 1, 1])

            with col1:
                st.write(row["Número do Processo"])
            with col2:
                st.write(row["Marca"])
            with col3:
                # Status na mesma linha
                status_editado = st.selectbox("", list(STATUS_MAP.values()), key=f"status_{i}", index=list(STATUS_MAP.values()).index(row['Status']), label_visibility="collapsed")
                if status_editado != row['Status']:
                    df_processos.loc[i, 'Status'] = status_editado
                    df_processos.loc[i, 'Código'] = [codigo for codigo, status in STATUS_MAP.items() if status == status_editado][0]
                    salvar_processos(df_processos)

            with col4:
                st.write(row["Apresentação"])
            with col5:
                st.write(row["Titular"])
            with col6:
                st.write(row["Classe"])
            with col7:
                confirm_exclusao = st.button(f"Excluir", key=f"delete_{i}")
                if confirm_exclusao:
                    st.session_state[f"confirm_delete_{i}"] = True

                if st.session_state.get(f"confirm_delete_{i}", False):
                    st.write(f"❗ Tem certeza que deseja excluir o processo {row['Número do Processo']}?")
                    if st.button("✅ Sim", key=f"confirm_delete_{i}_yes"):
                        df_processos = df_processos.drop(i).reset_index(drop=True)
                        salvar_processos(df_processos)
                        st.success(f"Processo {row['Número do Processo']} excluído com sucesso!")
                        del st.session_state[f"confirm_delete_{i}"]

                    if st.button("❌ Não", key=f"confirm_delete_{i}_no"):
                        del st.session_state[f"confirm_delete_{i}"]

    else:
        st.info("Nenhum processo cadastrado.")
