import pandas as pd

df = pd.read_csv('data/raw/news_preprocessed.csv')
df['pub_date'] = pd.to_datetime(df['pub_date'])

print(f'Rango de fechas: {df["pub_date"].min()} - {df["pub_date"].max()}')
print(f'Años: {df["pub_date"].dt.year.min()} - {df["pub_date"].dt.year.max()}')
print(f'\nDocumentos por año:')
print(df["pub_date"].dt.year.value_counts().sort_index())
