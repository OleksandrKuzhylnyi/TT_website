from sqlalchemy import create_engine
import pandas as pd

engine = create_engine("sqlite:///chess.db")

def slice_by_date(start=None, stop=None):
    query = "SELECT * FROM tournaments WHERE 1=1"

    if start:
        query += f" AND date >= '{start}'"
    if stop:
        query += f" AND date <= '{stop}'"

    df = pd.read_sql(query, engine)
    df['date'] = pd.to_datetime(df['date'])
    return df
