import sqlite3
from datetime import datetime

import pandas as pd
from sqlalchemy import create_engine, Column, String, Float, Integer
from sqlalchemy.orm import sessionmaker, declarative_base

"""
https://www.youtube.com/watch?v=W-g6StRy1zY

"""
# Criação do banco de dados
engine = create_engine("sqlite:///cotacoes.db")
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()


class Cotacao(Base):
    __tablename__ = 'cotacoes'
    id = Column('id', Integer, autoincrement=True)
    data = Column('Data', String)
    abertura = Column('Abertura', Float)
    maxima = Column('Maxima', Float)
    minima = Column('Minima', Float)
    max_min = Column('Max_Min', Float)

    def __init__(self):
        pass

Base.metadata.create_all(bind=engine)


def format_num_float(valor: str) -> float:
    valor_formatado = valor.replace(".", "").replace(",", ".")
    return float(valor_formatado)


# df = pd.read_csv("Mini Dolar Futuros Dados Historicos.csv", decimal=',')
# df = df[['Data', 'Abertura', 'Máxima', 'Mínima']]
# # print(df[:10])
# df['Abertura'] = df['Abertura'].apply(format_num_float)
# df['Máxima'] = df['Máxima'].apply(format_num_float)
# df['Mínima'] = df['Mínima'].apply(format_num_float)
# df['Max_Min'] = (df['Máxima']) - df['Mínima']
# print(df[:10])


# # Salva no banco (tabela 'cotacoes')
# df.to_sql("cotacoes", con=engine, if_exists="replace", index=False)

query = "SELECT Data, Máxima, Mínima, Max_Min FROM cotacoes ORDER BY rowid ASC LIMIT 20"
df_resultado = pd.read_sql(query, con=engine)
data_df = df_resultado.iloc[0]['Data']
dia, mes, ano = data_df.split('.')
data_datetime = datetime(int(ano), int(mes), int(dia))
data_datetime_df = data_datetime.date()
print(data_datetime_df)

# 18.08.2025
# data_hoje = datetime.now().strftime('%d.%m.%Y')
data_hoje = datetime.now().date()
print(data_hoje)
print(data_hoje == data_datetime_df)
