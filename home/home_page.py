import streamlit as st

from utils import calculo_acao, verificador_dia_util_b3


def home():
    st.markdown('# B3 - Ações')
    if verificador_dia_util_b3():
        st.badge("MERCADO ABERTO", icon=":material/check:", color="green", width="stretch")
        st.success('MERCADO ABERTO', icon="✅")
    else:
        st.error('MERCADO FECHADO! OS DADOS ESTÃO DESATUALIZADOS', icon="🚨")
    st.divider()
    ticker = st.text_input('Insira o código da ação:')
    btn_ticker = st.button('Calcular')
    if btn_ticker:
        if ticker:
            df_ticker, abertura_hoje, desvio_padrao_arredondado, df_lst_pontos_trade = calculo_acao(ticker)
            print(df_ticker)
            st.session_state['ticker'] = [df_ticker, abertura_hoje, desvio_padrao_arredondado, df_lst_pontos_trade]
            if abertura_hoje != 500:
                col1, col2, col3 = st.columns(3)
                linha, _ = df_ticker.shape
                st.markdown(f'# Ticker Selecionado: {ticker.upper()}')
                col1.metric(label='Abertura', value=round(abertura_hoje, 4))
                col2.metric(label='Desvio padrão', value=round(desvio_padrao_arredondado, 4))
                col3.metric(label='Dias selecionados', value=linha)
                st.markdown('# Pontos de Trade')
                st.dataframe(df_lst_pontos_trade, use_container_width=True)
                st.divider()
                st.markdown(f"## Dados da {ticker.upper()}")
                st.dataframe(df_ticker)
        else:
            st.error("NENHUM TICKER FOI INCERIDO!!!")
