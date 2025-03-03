import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter
import seaborn as sns


def get_data() -> pd.DataFrame:
    df = pd.read_csv("static/data.csv")
    return df


def make_barplot(df):
    first_places = df[df["place"] == 1]
    first = first_places["real_name"].value_counts()
    second_places = df[df["place"] == 2]
    second = second_places["real_name"].value_counts()
    third_places = df[df["place"] == 3]
    third = third_places["real_name"].value_counts()
    winners = pd.merge(first, second, how='outer', on="real_name", suffixes=('_1', '_2'))
    winners = pd.merge(winners, third, how='outer', on="real_name")
    winners.fillna(0, inplace=True)
    winners.reset_index(inplace=True)
    winners.rename(columns={"count_1" : '1', "count_2" : '2', "count" : '3'}, inplace=True)
    winners.sort_values(by=["1", "2", "3"], inplace=True)
    colors = ["yellow", "lightgrey", "brown"]
    winners.set_index("real_name").plot(kind='barh', stacked=True, color=colors, xticks=(np.arange(0, 12, 1)), figsize=(12,8))
    plt.savefig("static/barplot.png")
    plt.close() 


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


def plot_num_of_players(df):
    early = df[df["time"] == "E"]
    late = df[df["time"] == "L"]

    # Get max number of players per date
    num_of_players_E = early.groupby("date")["place"].max()
    num_of_players_L = late.groupby("date")["place"].max()

    # Plotting
    plt.figure(figsize=(12, 6))
    plt.plot(num_of_players_E.index, num_of_players_E.values, marker='o', label="Early Tournament", color='blue')
    plt.plot(num_of_players_L.index, num_of_players_L.values, marker='s', label="Late Tournament", color='red')
    plt.xlabel("Date")
    plt.ylabel("Number of Players")
    plt.title("Number of Players in Titled Tuesday (Early vs. Late)")
    plt.xticks(rotation=45)
    plt.legend()
    plt.grid(True)

    plt.savefig("static/max_players.png")
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


def players_by_participation(df, limit=100):
    top_participators = df["real_name"].value_counts()
    return top_participators[:limit].to_dict()


def average_score_of_winner(df):
    winners_df = df[df["place"] == 1]
    early = winners_df[winners_df["time"] == "E"]
    late = winners_df[winners_df["time"] == "L"]
    early_scores = early.loc[:, ["date", "Score"]].sort_values(by="date")
    late_scores = late.loc[:, ["date", "Score"]].sort_values(by="date")
    fig = plt.figure(figsize=(12, 6))
    plt.plot(early_scores["date"], early_scores["score"], label="Early", marker='o', color='blue')
    plt.plot(late_scores["date"], late_scores["score"], label="Late", marker='s', color='red')
    plt.legend()
    plt.xticks(rotation=45)
    plt.yticks(np.arange(9.5, 11.5, 0.5))
    plt.title("Score of the Winner over Time")
    plt.xlabel("Date")
    plt.ylabel("Score")
    plt.grid(True)

    plt.savefig("static/winner_score.png")
    plt.close()


def average_score_of_top_10(df):
    top_10_df = df[df["place"] <= 10]
    early = top_10_df[top_10_df["time"] == "E"]
    late = top_10_df[top_10_df["time"] == "L"]
    early_scores = early.loc[:, ["date", "score"]].groupby(["date"]).mean().sort_values(by="date")
    early_scores.reset_index(inplace=True)
    late_scores = late.loc[:, ["date", "score"]].groupby(["date"]).mean().sort_values(by="date")
    late_scores.reset_index(inplace=True)
    fig = plt.figure(figsize=(12, 6))
    plt.plot(early_scores["date"], early_scores["score"], label="Early", marker='o', color='blue')
    plt.plot(late_scores["date"], late_scores["score"], label="Late", marker='s', color='red')
    plt.legend()
    plt.xticks(rotation=45)
    plt.yticks(np.arange(9.5, 11.5, 0.5))
    plt.title("Score of the Winner over Time")
    plt.xlabel("Date")
    plt.ylabel("Score")
    plt.grid(True)

    plt.savefig("static/top_10_score.png")
    plt.close()


def average_rating_of_top_10(df):
    top_10_df = df[df["place"] <= 10]
    early = top_10_df[top_10_df["time"] == "E"]
    late = top_10_df[top_10_df["time"] == "L"]
    early_rating = early.loc[:, ["date", "rating"]].groupby(["date"]).mean().sort_values(by="date")
    early_rating.reset_index(inplace=True)
    late_rating = late.loc[:, ["date", "rating"]].groupby(["date"]).mean().sort_values(by="date")
    late_rating.reset_index(inplace=True)
    fig = plt.figure(figsize=(12, 6))
    plt.plot(early_rating["date"], early_rating["rating"], label="Early", marker='o', color='blue')
    plt.plot(late_rating["date"], late_rating["rating"], label="Late", marker='s', color='red')
    plt.legend()
    plt.xticks(rotation=45)
    plt.yticks(np.arange(2950, 3200, 50))
    plt.title("Average Rating of Top 10 over Time")
    plt.xlabel("Date")
    plt.ylabel("Rating")
    plt.grid(True)

    plt.savefig("static/top_10_rating.png")
    plt.close()
    

def skips_per_round(df):
    num_games = df.shape[0]
    skips = [(df[f"round_{i}"] == "U--").sum() / num_games for i in range(1, 12)]
    fig = plt.figure(figsize=(12, 6))
    plt.bar(np.arange(1, 12), skips, color='blue')
    plt.xticks(np.arange(1, 12))
    plt.title("Percent of Skips per Round")
    plt.xlabel("Round")
    plt.ylabel("Percent of Skips")
    plt.gca().yaxis.set_major_formatter(PercentFormatter(1))

    plt.savefig("static/skips_per_round.png")
    plt.close()

def starting_ranks_of_winners(df):
    starting_rankings = df[df["place"] == 1]["starting_rank"]
    bins = [0, 1, 2, 3, 5, 10, 20, 50, float("inf")]
    labels = ["1", "2", "3", "4-5", "6-10", "11-20", "21-50", "50+"]
    categories = pd.cut(starting_rankings, bins=bins, labels=labels, right=True)
    category_counts = categories.value_counts().sort_index()

    plt.figure(figsize=(8, 8))
    plt.pie(category_counts, labels=category_counts.index, autopct="%1.1f%%", startangle=140, colors=plt.cm.Paired.colors)
    plt.title("Proportion of Winners by Starting Position")

    plt.savefig("static/starting_ranks.png")
    plt.close()

starting_ranks_of_winners(get_data())