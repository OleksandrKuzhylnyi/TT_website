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
    color_map = {1: 'yellow', 2: 'lightgrey', 3: 'brown', 4: 'red', 5: 'red',
                 6: 'green', 7: 'green', 8: 'green', 9: 'green', 10: 'green'}
    colors = [color_map.get(rank, 'blue') for _, rank in rankings_by_date]
    plt.figure(figsize=(14, 8))
    plt.scatter(*zip(*rankings_by_date), c=colors, alpha=0.5)
    plt.xticks(df_player["date"].values, rotation=45)
    plt.title(f"Rankings of {player}")
    plt.ylabel("Ranking")

    handles = [
        plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='yellow', markersize=10, label='1st'),
        plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='lightgrey', markersize=10, label='2nd'),
        plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='brown', markersize=10, label='3rd'),
        plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='red', markersize=10, label='4th or 5th'),
        plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='green', markersize=10, label='6th to 10th'),
        plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='blue', markersize=10, label='11th or worse')
    ]

    plt.legend(handles=handles, loc='center right')
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


def analyze_player_performance(df: pd.DataFrame, player="Hikaru Nakamura") -> dict:
    """
    Analyzes the performance of a specific player.
    """
    player_df = df[df["Name"] == player]

    max_possible_games = player_df.shape[0] * 11
    rounds = player_df.loc[:, "RND1":"RND11"].columns
    wins = sum([player_df[round].str.startswith("W").sum() for round in rounds])
    draws = sum([player_df[round].str.startswith("D").sum() for round in rounds])
    losses = sum([player_df[round].str.startswith("L").sum() for round in rounds])
    number_of_games = wins + draws + losses
    skipped_games = max_possible_games - number_of_games

    first = player_df[df["Number"] == 1].shape[0]
    second = player_df[df["Number"] == 2].shape[0]
    third = player_df[df["Number"] == 3].shape[0]
    top5 = player_df[df["Number"] <= 5].shape[0]
    top10 = player_df[df["Number"] <= 10].shape[0]
    top100 = player_df[df["Number"] <= 100].shape[0]

    results = {
        "player": player,
        "max_possible_games": max_possible_games,
        "skipped_games": skipped_games,
        "real_number_of_games": number_of_games,
        "wins": wins,
        "draws": draws,
        "losses": losses,
        "percent_of_points": 100 * (wins + draws / 2) / number_of_games,
        "percent_of_wins": 100 * wins / number_of_games,
        "percent_of_draws": 100 * draws / number_of_games,
        "percent_of_losses": 100 * losses / number_of_games,
        "first_place": first,
        "second_place": second,
        "third_place": third,
        "top5": top5,
        "top10": top10,
        "top100": top100,
    }

    return results


def main():
    df = get_data()
    make_barplot(df)
    plot_player_ranking(df)
    plot_num_of_players(df)
    analyze_player_performance(df, "Hikaru Nakamura")

if __name__ == "__main__":
    main()
