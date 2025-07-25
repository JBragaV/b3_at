from utils import calculo_acao, calcular_pontos_de_trade, formatador_abertura_usuario

lst_ticker = ['PETR4', 'VALE3', 'CPFE3', 'Wdofut', 'Winfut']
if __name__ == '__main__':
    ticker = lst_ticker[2]
    if ticker in ['Wdofut', 'Winfut']:
        abertura_user = formatador_abertura_usuario(input(f"Qual a abertura do {ticker.upper()}"))
        df, _, desvio_padrao = calculo_acao(ticker)
        abertura = abertura_user
    else:
        df, abertura, desvio_padrao = calculo_acao(ticker)

    if abertura != 500 and not isinstance(abertura, int):
        print(df)
        lista_trade = calcular_pontos_de_trade(desvio_padrao, float(abertura))
        print(f'Ticker: {ticker}')
        print(f'Abertura: {abertura}', f'Desvio Padrão: {desvio_padrao}')
        for i, ponto in enumerate(lista_trade):
            print(f'Ponto {i+1}: {abertura} + Desvio Padrão x {i+1}: {ponto[0]} '
                  f'--- {abertura} - Desvio Padrão x {i+1}: {ponto[1]}')
    else:
        print(desvio_padrao)
