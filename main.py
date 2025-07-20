from utils import calculo_acao, calcular_pontos_de_trade

lst_ticker = ['PETR4', 'Wdofut', 'Winfut']
if __name__ == '__main__':
    ticker = lst_ticker[0]
    df, abertura, desvio_padrao = calculo_acao(ticker)
    if abertura != 500:
        print(df)
        lista_trade = calcular_pontos_de_trade(desvio_padrao, float(abertura))
        print(f'Ticker: {ticker}')
        print(f'Abertura: {abertura}', f'Desvio Padrão: {desvio_padrao}')
        for i, ponto in enumerate(lista_trade):
            print(f'Ponto {i+1}: {abertura} + Desvio Padrão x {i+1}: {ponto[0]} '
                  f'--- {abertura} - Desvio Padrão x {i+1}: {ponto[1]}')
    else:
        print(desvio_padrao)
