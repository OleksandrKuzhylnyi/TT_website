import pandas as pd

def slice_by_date(df, start=None, stop=None):
    start = start or df['date'].min()
    stop = stop or df['date'].max()
    return df[(df['date'] >= start) & (df['date'] <= stop)]