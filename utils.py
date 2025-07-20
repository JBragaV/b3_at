from datetime import datetime, timedelta
import math

import pandas as pd
from playwright.sync_api import sync_playwright
import yfinance as yf


def arredondar_marred_0_5(numero):
    """Arredonda um número para o múltiplo de 0.5 mais próximo."""
    return round(numero * 2) / 2


def buscador_acao(ticker: str):
    ticker_formatado = ticker.upper() if ticker.upper().endswith('.SA') else f'{ticker.upper()}.SA'
    dat = yf.Ticker(ticker_formatado)
    return dat


def tratador_dados_acao(dat):
    df_ticker = dat.history().sort_index(ascending=False).head(21)[['Open', 'High', 'Low', 'Close']]
    abertura_hoje = df_ticker.iloc[0]['Open']
    df_ticker.loc[:, 'Max-Min'] = df_ticker['High'] - df_ticker['Low']
    df_ticker_formatted = df_ticker.map(lambda x: round(float(x), 2))
    return df_ticker_formatted.iloc[1:], round(float(abertura_hoje), 2)


def calculo_acao(ticker: str) -> tuple:
    try:
        dat = buscador_acao(ticker.upper())
        df_ticker, abertura_hoje = tratador_dados_acao(dat)
    except Exception:
        try:
            df_ticker, abertura_hoje = tratador_df_raspagem(ticker.upper())
        except Exception:
            return 'Erro', 500, f'Não foi possivel encontar os valores do ticker {ticker}'
    desvio_padrao_max_min = df_ticker['Max-Min'].std()
    desvio_padrao_arredondado = arredondar_marred_0_5(desvio_padrao_max_min)
    return df_ticker, abertura_hoje, desvio_padrao_arredondado


def br_to_float(txt: str) -> float:
    return float(txt.replace('.', '').replace(',', '.'))


def tratador_df_raspagem(ticker):
    dados = raspador_indices(ticker)
    df = pd.DataFrame(dados).dropna(subset=["Data"])
    df = df.set_index("Data").sort_index(ascending=False).head(21)
    abertura_hoje = df.iloc[0]['Abertura']
    df = df.map(lambda x: round(float(x), 2))
    df.loc[:, 'Max-Min'] = df['Máxima'] - df['Mínima']
    return df.iloc[1:], abertura_hoje


def raspador_indices(ticker='WDOFUT') -> list:
    print('Iniciando a raspagem')
    url = f'https://br.advfn.com/bolsa-de-valores/bmf/{ticker}/historico'
    with sync_playwright() as p:
        with p.chromium.launch(headless=True) as browser:
            page = browser.new_page(user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"))
            page.goto(url, timeout=60000)

            # Aguarda a tabela com pelo menos uma linha e a coluna Date
            page.wait_for_selector('div[col-id="Date"] span', timeout=600000)

            rows = page.locator('div.ag-center-cols-container > div[role="row"]')
            total_rows = rows.count()
            print(f"Total de linhas encontradas: {total_rows}")

            data = []

            for i in range(total_rows):
                r = rows.nth(i)
                r.scroll_into_view_if_needed()
                try:
                    date_txt = r.locator('div[col-id="Date"] span').inner_text(timeout=5000)
                    open_txt = r.locator('div[col-id="OpenPrice"] span').inner_text(timeout=5000)
                    close_txt = r.locator('div[col-id="ClosePrice"] span').inner_text(timeout=5000)
                    high_txt = r.locator('div[col-id="HighPrice"] span').inner_text(timeout=5000)
                    low_txt = r.locator('div[col-id="LowPrice"] span').inner_text(timeout=5000)

                    data.append({
                        "Data": pd.to_datetime(date_txt, dayfirst=True, errors='coerce'),
                        "Abertura": br_to_float(open_txt),
                        "Fechamento": br_to_float(close_txt),
                        "Máxima": br_to_float(high_txt),
                        "Mínima": br_to_float(low_txt)
                    })
                except Exception as e:
                    continue
    return data


def calcular_pontos_de_trade(std, abertura):
    lst_pontos_trade = []
    for i in range(1, 5):
        lst_pontos_trade.append(
                (
                    round(abertura + (std * i), 2), round(abertura - (std * i), 2)
                )
            )
    return lst_pontos_trade
