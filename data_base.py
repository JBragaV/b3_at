import sqlite3

import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

"""
https://www.youtube.com/watch?v=W-g6StRy1zY

"""


def format_num_float(valor: str) -> float:
    valor_formatado = valor.replace(".", "").replace(",", ".")
    return float(valor_formatado)


df = pd.read_csv("Mini Dólar Futuros Dados Históricos.csv", decimal=',')
df = df[['Data', 'Abertura', 'Máxima', 'Mínima']]
# df['Max-Min'] = (df['Máxima']) - df['Mínima']
print(df[:10])
print(df['Máxima'].apply(format_num_float))
# Criação do banco de dados
# engine = create_engine("sqlite:///cotacoes.db")
#
# # Salva no banco (tabela 'cotacoes')
# df.to_sql("cotacoes", con=engine, if_exists="replace", index=False)

# query = "SELECT Data, Máxima, Mínima, Max-Min FROM cotacoes ORDER BY rowid ASC LIMIT 20"
# df_resultado = pd.read_sql(query, con=engine)
# print(df_resultado)
