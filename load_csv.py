import pandas as pd
from sqlalchemy import create_engine
from models import OKS, Base

CSV_PATH = '2025_03_data/03_OKS.csv'
DB_URL = 'sqlite:///oks.db'

def load_csv_to_db():
    df = pd.read_csv(CSV_PATH, encoding='utf-8', sep=';', header=0, dtype=str)
    df.dropna(subset=['Наименование'], inplace=True)
    df.reset_index(drop=True, inplace=True)

    cols_to_fill = ["Класс", "Подкласс 1", "Подкласс 2"]
    df[cols_to_fill] = df[cols_to_fill].ffill()

    df.set_index('УИН', inplace=True, drop=True)
    df.fillna('', inplace=True)  # теперь dtype=str, и fillna('') безопасно

    engine = create_engine(DB_URL)
    Base.metadata.create_all(engine)

    df.to_sql('oks', engine, if_exists='replace', index_label='УИН')

if __name__ == '__main__':
    load_csv_to_db()
