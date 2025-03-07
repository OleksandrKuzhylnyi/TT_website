import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def plot_player_ranking(df, player="Hikaru Nakamura"):
    df_player = df[df["real_name"] == player]
    rankings_by_date = list(zip(df_player["date"].values, df_player["place"].values))
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
