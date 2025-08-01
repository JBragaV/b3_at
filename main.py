import streamlit as st

from utils import calculo_acao


def home():
    st.markdown('# B3 - Ações')
    st.divider()
    ticker = st.text_input('Insira o código da ação:')
    btn_ticker = st.button('Calcular')
    if btn_ticker:
        df_ticker, abertura_hoje, desvio_padrao_arredondado, df_lst_pontos_trade = calculo_acao(ticker)
        if abertura_hoje != 500:
            col1, col2, col3 = st.columns(3)
            linha, _ = df_ticker.shape
            st.markdown(f'# Ticker Selecionado: {ticker.upper()}')
            col1.metric(label='Abertura', value=abertura_hoje)
            col2.metric(label='Desvio padrão', value=desvio_padrao_arredondado)
            col3.metric(label='Dias selecionados', value=linha)
            st.markdown('# Pontos de Trade')
            st.dataframe(df_lst_pontos_trade)
            st.divider()
            st.markdown(f"## Dados da {ticker.upper()}")
            st.dataframe(df_ticker)


home()
