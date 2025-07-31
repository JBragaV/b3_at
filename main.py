import streamlit as st

from utils import calculo_acao


def home():
    st.markdown('# B3 - Ações')
    st.divider()
    ticker = st.text_input('Insira o código da ação:')
    btn_ticker = st.button('Calcular')
    if btn_ticker:
        df_ticker, abertura_hoje, desvio_padrao_arredondado = calculo_acao(ticker)
        if abertura_hoje != 500:
            col1, col2 = st.columns(2)
            col1.metric(label=f'Abertura da {ticker.upper()}', value=abertura_hoje)
            col2.metric(label=f'Desvio padrão da {ticker.upper()}', value=desvio_padrao_arredondado)
            linha, _ = df_ticker.shape
            st.markdown(f"## Quantidade de dias selecionada: {linha}")
            st.dataframe(df_ticker)


home()
