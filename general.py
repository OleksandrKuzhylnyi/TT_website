from sqlalchemy import create_engine
import pandas as pd
from time import time

def timer_func(func): 
    def wrap_func(*args, **kwargs): 
        t1 = time() 
        result = func(*args, **kwargs) 
        t2 = time() 
        print(f'Function {func.__name__!r} executed in {(t2-t1):.4f}s') 
        return result 
    return wrap_func 


def slice_by_date(df, start=None, stop=None):
    if start:
        df = df[df['date'] >= pd.to_datetime(start)]
    if stop:
        df = df[df['date'] <= pd.to_datetime(stop)]
    return df
