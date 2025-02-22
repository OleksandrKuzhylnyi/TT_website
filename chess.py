import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


def get_data() -> pd.DataFrame:
    df = pd.read_csv("static/data.csv")
    return df

def make_barplot(df):
    first_places = df[df["Number"] == 1]
    first = first_places["Name"].value_counts()
    second_places = df[df["Number"] == 2]
    second = second_places["Name"].value_counts()
    third_places = df[df["Number"] == 3]
    third = third_places["Name"].value_counts()
    winners = pd.merge(first, second, how='outer', on="Name", suffixes=('_1', '_2'))
    winners = pd.merge(winners, third, how='outer', on="Name")
    winners.fillna(0, inplace=True)
    winners.reset_index(inplace=True)
    winners.rename(columns={"count_1" : '1', "count_2" : '2', "count" : '3'}, inplace=True)
    winners.sort_values(by=["1", "2", "3"], inplace=True)
    colors = ["yellow", "lightgrey", "brown"]
    winners.set_index("Name").plot(kind='barh', stacked=True, color=colors, xticks=(np.arange(0, 12, 1)), figsize=(12,8))
    plt.savefig("static/barplot.png")
    plt.close() 


def plot_player_ranking(df, player="Hikaru Nakamura"):
    df_player = df[df["Name"] == player]
    rankings_by_date = list(zip(df_player["date"].values, df_player["Number"].values))
    rankings_by_date.sort()
    color_map = {1: 'yellow', 2: 'lightgrey', 3: 'brown'}
    colors = [color_map.get(rank, 'blue') for _, rank in rankings_by_date]
    plt.figure(figsize=(14, 8))
    plt.scatter(*zip(*rankings_by_date), c=colors)
    plt.xticks(df_player["date"].values, rotation=45)
    plt.title(f"Rankings of {player}")
    plt.ylabel("Ranking")
    plt.savefig(f"static/{player.replace(' ', '_')}_ranking.png")
    plt.close()


def plot_num_of_players(df):
    # Separate Early and Late tournaments
    early = df[df["time"] == "E"]
    late = df[df["time"] == "L"]

    # Get max number of players per date
    num_of_players_E = early.groupby("date")["Number"].max()
    num_of_players_L = late.groupby("date")["Number"].max()

    # Plotting
    plt.figure(figsize=(12, 6))
    plt.plot(num_of_players_E.index, num_of_players_E.values, marker='o', label="Early Tournament", color='blue')
    plt.plot(num_of_players_L.index, num_of_players_L.values, marker='s', label="Late Tournament", color='red')

    # Formatting
    plt.xlabel("Date")
    plt.ylabel("Number of Players")
    plt.title("Number of Players in Titled Tuesday (Early vs. Late)")
    plt.xticks(rotation=45)
    plt.legend()
    plt.grid(True)

    plt.savefig("static/max_players.png")
    plt.close()


def main():
    df = get_data()
    make_barplot(df)
    plot_player_ranking(df)
    plot_num_of_players(df)

if __name__ == "__main__":
    main()
