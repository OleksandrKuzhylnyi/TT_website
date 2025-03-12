import pandas as pd
from sqlalchemy import create_engine

# Load CSV
df = pd.read_csv("static/data.csv")

# Create SQLite engine (creates a file called chess.db)
engine = create_engine("sqlite:///chess.db", echo=True)

# Save DataFrame to SQL table
df.to_sql("tournaments", con=engine, if_exists="replace", index=False)

print("Database created and data imported!")
