import os
import re
from datetime import datetime
import pandas as pd

def rename_chess_files(directory="H:\\TT\\results\\TODO\\"):
    for filename in os.listdir(directory):
        if not filename.endswith('.csv'):
            continue
            
        # Extract date using regex
        match = re.search(r'(?:early|late)-titled-tuesday-blitz-(\w+-\d{2}-\d{4})', filename)
        if not match:
            continue
            
        # Parse the date
        date_str = match.group(1)
        date_obj = datetime.strptime(date_str, '%B-%d-%Y')
        
        # Format new date as DD.MM.YY
        new_date = date_obj.strftime('%d.%m.%y')
        
        # Determine if it's early or late tournament
        prefix = 'ETT' if filename.startswith('early') else 'LTT'
        
        # Create new filename
        new_filename = f"{prefix}_{new_date}.csv"
        
        # Rename the file
        old_path = os.path.join(directory, filename)
        new_path = os.path.join(directory, new_filename)
        
        try:
            os.rename(old_path, new_path)
            print(f"Renamed: {filename} -> {new_filename}")
        except OSError as e:
            print(f"Error renaming {filename}: {e}")

def get_data():
    df = pd.DataFrame()
    folder_path = "H:\\TT\\results\\"
    file_list = os.listdir(folder_path)
    for file in file_list:
        file_path = os.path.join(folder_path, file)
        raw = pd.read_csv(file_path)
        raw.insert(0, "date", file[4:12])
        raw.insert(0, "time", file[0])
        raw.insert(0, "tournament", file[:12])
        df = pd.concat([df, raw], ignore_index=True)
    df.drop(columns=["Fed"], inplace=True)  # Doesn't represent player's federation correctly
    df.rename(columns={
    "Number": "place",
    "Rk": "starting_rank",
    "Title": "title",
    "Username": "username",
    "Name": "real_name",
    "Rating": "rating",
    "Score": "score",
    "Buchholz Cut 1": "buchholz_cut_1",
    "Buchholz": "buchholz",
    "Sonneborn-Berger": "sonneborn_berger",
    "Direct encounter": "direct_encounter",
    "The greater number of wins including forfeits": "wins_count",
    "Number of wins with Black pieces": "black_wins_count",
    "AROC 1": "aroc_1",
    **{f"RND{i}": f"round_{i}" for i in range(1, 12)}  # Rename RND1-RND11 dynamically
    }, inplace=True)
    df["date"] = pd.to_datetime(df["date"], format="%d.%m.%y")
    df.to_csv("static/data.csv", index=False)

if __name__ == "__main__":
    get_data()
