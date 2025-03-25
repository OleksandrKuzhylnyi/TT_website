from collections import Counter, defaultdict
from dataclasses import dataclass
from itertools import combinations
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


@dataclass
class Results:
    wins: int = 0
    draws: int = 0
    losses: int = 0

    def __add__(self, other):
        if not isinstance(other, Results):
            raise TypeError
        return Results(
            self.wins + other.wins,
            self.draws + other.draws,
            self.losses + other.losses
        )
    
    def __invert__(self):
        return(Results(wins=self.losses, draws=self.draws, losses=self.wins))

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
    plt.scatter(*zip(*rankings_by_date), c=colors, figure=plt.figure(figsize=(16, 12)))
    dates = sorted(df_player["date"].unique())
    plt.xticks(dates[::2], rotation=45)
    plt.title(f"Rankings of {player}")
    plt.ylabel("Ranking (Log Scale)")
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
    plt.savefig(f"static/images/{player.replace(' ', '_')}_ranking.png")
    plt.close()

def analyze_player_performance(df, player="Hikaru Nakamura") -> dict:
    """
    Analyzes the performance of a specific player.
    """
    player_df = df[df["real_name"] == player]

    tournaments_count = player_df["tournament"].nunique()
    first_tournament = player_df["date"].min().strftime("%Y-%m-%d")
    last_tournament = player_df["date"].max().strftime("%Y-%m-%d")

    max_possible_games = player_df.shape[0] * 11
    rounds = player_df.loc[:, "round_1":"round_11"].columns
    wins = sum([player_df[round].str.startswith("W").sum() for round in rounds])
    draws = sum([player_df[round].str.startswith("D").sum() for round in rounds])
    losses = sum([player_df[round].str.startswith("L").sum() for round in rounds])
    played_games = wins + draws + losses
    skipped_games = max_possible_games - played_games

    first = player_df[player_df["place"] == 1].shape[0]
    second = player_df[player_df["place"] == 2].shape[0]
    third = player_df[player_df["place"] == 3].shape[0]
    top5 = player_df[player_df["place"] <= 5].shape[0]
    top10 = player_df[player_df["place"] <= 10].shape[0]
    top100 = player_df[player_df["place"] <= 100].shape[0]

    mean_place = player_df["place"].mean()
    median_place = player_df["place"].median()

    results = {
        "player": player,
        "tournaments_count": tournaments_count,
        "first_tournament": first_tournament,
        "last_tournament": last_tournament,
        "max_possible_games": max_possible_games,
        "played_games": played_games,
        "skipped_games": skipped_games,
        "wins": wins,
        "draws": draws,
        "losses": losses,
        "percent_of_points": 100 * (wins + draws / 2) / played_games,
        "percent_of_wins": 100 * wins / played_games,
        "percent_of_draws": 100 * draws / played_games,
        "percent_of_losses": 100 * losses / played_games,
        "first_place": first,
        "second_place": second,
        "third_place": third,
        "top5": top5,
        "top10": top10,
        "top100": top100,
        "mean_place": mean_place,
        "median_place": median_place
    }

    return results


def analyze_performance_by_rounds(df, player="Hikaru Nakamura") -> dict:
    """
    Analyzes the performance of a specific player by rounds.
    """
    player_df = df[df["real_name"] == player]

    rounds = [f"round_{i}" for i in range(1, 12)]
    wins_draws_losses = [
        (
        player_df[round].str.startswith("W").sum(),
        player_df[round].str.startswith("D").sum(),
        player_df[round].str.startswith("L").sum()
        )
        for round in rounds
    ]
    wins, draws, losses = zip(*wins_draws_losses)
    max_possible_games = player_df.shape[0]
    played_games = [wins + draws + losses for wins, draws, losses in wins_draws_losses]
    skipped_games = [max_possible_games - games for games in played_games]

    results = [
        {
            "played_games": played_games[i],
            "skipped_games": skipped_games[i],
            "wins": wins[i],
            "draws": draws[i],
            "losses": losses[i],
            "percent_of_points": 100 * (wins[i] + draws[i] / 2) / played_games[i],
            "percent_of_wins": 100 * wins[i] / played_games[i],
            "percent_of_draws": 100 * draws[i] / played_games[i],
            "percent_of_losses": 100 * losses[i] / played_games[i],
        }
        for i in range(11)
    ]

    return results


def get_opponents_in_tournament(df, place: int) -> dict:
    """
    Returns dict of results against opponents of player by place in specific tournament.
    """
    row = df[df["place"] == place].iloc[0]
    rounds = [f"round_{i}" for i in range(1, 12)]
    results = [row[round] for round in rounds if row[round] != "U--" and row[round] != "BYE"]
    wins_places = []
    draws_places = []
    losses_places = []
    for result in results:
        outcome = result[0]
        place = int(result[1:-1])
        if outcome == "W":
            wins_places.append(place)
        elif outcome == "D":
            draws_places.append(place)
        elif outcome == "L":
            losses_places.append(place)

    wins = None
    draws = None
    losses = None

    if wins_places:
      wins = list(df[df['place'].isin(wins_places)]['real_name'])
    if draws_places:
      draws = list(df[df['place'].isin(draws_places)]['real_name'])
    if losses_places:
      losses = list(df[df['place'].isin(losses_places)]['real_name'])

    return {
        "wins" : wins,
        "draws" : draws,
        "losses" : losses
    }


def get_opponents(df, player="Hikaru Nakamura") -> dict:
    """
    Returns dict of results against all opponents of the player.
    """
    dfs_by_tournament = {}
    grouped = df.groupby('tournament')
    for tournament, group_df in grouped:
        dfs_by_tournament[tournament] = group_df

    places = []
    for tournament in dfs_by_tournament.values():
        if player in tournament["real_name"].values:
            places.append(tournament[tournament["real_name"] == player]["place"].iloc[0])
        else:
            places.append(None)

    opponents = {
        "wins" : [],
        "draws" : [],
        "losses" : []
    }
    for tournament, place in zip(dfs_by_tournament.values(), places):
        if place:
            tournament_opponents = get_opponents_in_tournament(tournament, place)
            for result in opponents:
                if tournament_opponents[result]:
                  opponents[result].extend(tournament_opponents[result])

    for result in opponents:
        # Some players didn't enter their name.
        opponents[result] = [player for player in opponents[result] if isinstance(player, str)]

    return opponents


def analyze_opponents(df, player="Hikaru Nakamura"):
    opponents = get_opponents(df, player)
    wins = Counter(opponents["wins"]).most_common(5)
    draws = Counter(opponents["draws"]).most_common(5)
    losses = Counter(opponents["losses"]).most_common(5)

    return Results(wins, draws, losses)


def head_to_head(df, players):
    results = {}
    total = defaultdict(lambda: Results())
        
    for player, opponent in combinations(players, 2):
        opponents = get_opponents(df, player)
        wins = opponents["wins"].count(opponent)
        draws = opponents["draws"].count(opponent)
        losses = opponents["losses"].count(opponent)
        results[(player, opponent)] = Results(wins, draws, losses)

        total[player] += Results(wins, draws, losses)
        total[opponent] += ~Results(wins, draws, losses) # Wins and losses are switched.

    return results, total