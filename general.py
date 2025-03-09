import pandas as pd

def slice_by_date(df, start="2000-01-01", stop="2030-01-01"):
    return df[(df['date'] >= start) & (df['date'] <= stop)]