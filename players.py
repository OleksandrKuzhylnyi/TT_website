import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def get_color(rank):
    if rank == 1:
        return 'gold'
    elif rank == 2:
        return 'silver'
    elif rank == 3:
        return 'brown'
    elif 4 <= rank <= 5:
        return 'lime'
    elif 6 <= rank <= 10:
        return 'aqua'
    elif 11 <= rank <= 20:
        return 'red'
    elif 21 <= rank <= 50:
        return 'green'
    elif 51 <= rank <= 100:
        return 'blue'
    elif 101 <= rank <= 200:
        return 'darkorange'
    elif 201 <= rank <= 300:
        return 'purple'
    elif 301 <= rank <= 400:
        return 'magenta'
    elif 401 <= rank <= 500:
        return 'khaki'
    else:
        return 'black'  # For rankings worse than 500


def plot_player_ranking(df, player="Hikaru Nakamura"):
    df_player = df[df["real_name"] == player]
    rankings_by_date = list(zip(df_player["date"].values, df_player["place"].values))
    rankings_by_date.sort()
    colors = [get_color(rank) for _, rank in rankings_by_date]
    plt.figure(figsize=(16, 12))
    plt.scatter(*zip(*rankings_by_date), c=colors)
    dates = sorted(df_player["date"].unique())
    plt.xticks(dates[::2], rotation=45)
    plt.title(f"Rankings of {player}")
    plt.ylabel("Ranking")
    plt.yscale("log")
    plt.yticks([1, 2, 3, 5, 10, 20, 50, 100, 200, 300, 400, 500], [1, 2, 3, 5, 10, 20, 50, 100, 200, 300, 400, 500])

    handles = [
        plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='gold', markersize=10, label='1'),
        plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='silver', markersize=10, label='2'),
        plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='brown', markersize=10, label='3'),
        plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='lime', markersize=10, label='4 to 5'),
        plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='aqua', markersize=10, label='6 to 10'),
        plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='red', markersize=10, label='11 to 20'),
        plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='green', markersize=10, label='21 to 50'),
        plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='blue', markersize=10, label='51 to 100'),
        plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='darkorange', markersize=10, label='101 to 200'),
        plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='purple', markersize=10, label='201 to 300'),
        plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='magenta', markersize=10, label='301 to 400'),
        plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='khaki', markersize=10, label='401 to 500'),
        plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='black', markersize=10, label='500+')
    ]

    plt.legend(handles=handles, title="Ranking", loc="best")
    plt.tight_layout()
    plt.savefig(f"static/{player.replace(' ', '_')}_ranking.png")
    plt.close()

def analyze_player_performance(df, player="Hikaru Nakamura") -> dict:
    """
    Analyzes the performance of a specific player.
    """
    player_df = df[df["real_name"] == player]

    max_possible_games = player_df.shape[0] * 11
    rounds = player_df.loc[:, "round_1":"round_11"].columns
    wins = sum([player_df[round].str.startswith("W").sum() for round in rounds])
    draws = sum([player_df[round].str.startswith("D").sum() for round in rounds])
    losses = sum([player_df[round].str.startswith("L").sum() for round in rounds])
    number_of_games = wins + draws + losses
    skipped_games = max_possible_games - number_of_games

    first = player_df[player_df["place"] == 1].shape[0]
    second = player_df[player_df["place"] == 2].shape[0]
    third = player_df[player_df["place"] == 3].shape[0]
    top5 = player_df[player_df["place"] <= 5].shape[0]
    top10 = player_df[player_df["place"] <= 10].shape[0]
    top100 = player_df[player_df["place"] <= 100].shape[0]

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
