import pandas as pd
from sqlalchemy import create_engine, text

df = pd.read_csv("static/data.csv")
df['date'] = pd.to_datetime(df['date']).dt.date

engine = create_engine("sqlite:///chess.db")

df.to_sql("tournaments", con=engine, if_exists="replace", index=False)

# Create indexes for performance
with engine.connect() as conn:
    conn.execute(text("CREATE INDEX IF NOT EXISTS idx_name ON tournaments (real_name)"))
    conn.execute(text("CREATE INDEX IF NOT EXISTS idx_date ON tournaments (date)"))
    conn.execute(text("CREATE INDEX IF NOT EXISTS idx_placement ON tournaments (place)"))
    conn.execute(text("CREATE INDEX IF NOT EXISTS idx_time ON tournaments (time)"))

print("Database created successfully.")
