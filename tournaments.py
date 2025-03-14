import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def plot_num_of_players(df):
    early = df[df["time"] == "E"]
    late = df[df["time"] == "L"]

    # Get number of players per date
    num_of_players_E = early.groupby("date")["place"].max()
    num_of_players_L = late.groupby("date")["place"].max()

    plt.figure(figsize=(12, 6))
    plt.plot(num_of_players_E.index, num_of_players_E.values, marker='o', markersize=5,
             label="Early Tournament", color='blue')
    plt.plot(num_of_players_L.index, num_of_players_L.values, marker='s', markersize=5, 
             label="Late Tournament", color='red')
    plt.ylabel("Number of Players")
    plt.title("Number of Players in Titled Tuesday (Early vs. Late)")
    plt.xticks(num_of_players_E.index[::2], rotation=45)
    plt.legend()
    plt.grid(True, linestyle='--', linewidth=0.5, alpha=0.7)
    plt.tight_layout()
    plt.gca().set_facecolor('#f9f9f9')
    plt.savefig("static/pictures/num_of_players.png")
    plt.close()

def average_score_of_winner(df):
    winners_df = df[df["place"] == 1]
    early = winners_df[winners_df["time"] == "E"]
    late = winners_df[winners_df["time"] == "L"]
    early_scores = early.loc[:, ["date", "score"]].sort_values(by="date")
    late_scores = late.loc[:, ["date", "score"]].sort_values(by="date")
    fig = plt.figure(figsize=(12, 6))
    plt.plot(early_scores["date"], early_scores["score"], label="Early", marker='o', color='blue')
    plt.plot(late_scores["date"], late_scores["score"], label="Late", marker='s', color='red')
    plt.legend()
    plt.xticks(early_scores["date"][::2], rotation=45)
    plt.yticks(np.arange(9.5, 11.5, 0.5))
    plt.title("Score of the Winner over Time")
    plt.ylabel("Score")
    plt.grid(True, linestyle='--', linewidth=0.5, alpha=0.7)
    plt.tight_layout()
    plt.gca().set_facecolor('#f9f9f9')
    plt.savefig("static/pictures/winner_score.png")
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
    plt.xticks(early_scores["date"][::2], rotation=45)
    plt.yticks(np.arange(8.5, 10.5, 0.5))
    plt.title("Average Score of top 10 over Time")
    plt.ylabel("Score")
    plt.grid(True, linestyle='--', linewidth=0.5, alpha=0.7)
    plt.tight_layout()
    plt.gca().set_facecolor('#f9f9f9')
    plt.savefig("static/pictures/top_10_score.png")
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
    plt.xticks(early_rating["date"][::2], rotation=45)
    plt.yticks(np.arange(2950, 3200, 50))
    plt.title("Average Rating of Top 10 over Time")
    plt.ylabel("Rating")
    plt.grid(True, linestyle='--', linewidth=0.5, alpha=0.7)
    plt.gca().set_facecolor('#f9f9f9')
    plt.tight_layout()
    plt.savefig("static/pictures/top_10_rating.png")
    plt.close()

def skips_per_round(df):
    num_games = df.shape[0]
    skips = [(df[f"round_{i}"] == "U--").sum() / num_games for i in range(1, 12)]
    fig = plt.figure(figsize=(12, 6))
    plt.bar(np.arange(1, 12), skips, color='royalblue', edgecolor='black', alpha=0.8)
    for i, v in enumerate(skips):
        plt.text(i + 1, v + 0.005, f"{v:.1%}", ha='center', fontsize=10, color='black')
    plt.xticks(np.arange(1, 12))
    plt.title("Percent of Skips per Round")
    plt.xlabel("Round")
    plt.yticks([])
    plt.gca().set_facecolor('#f9f9f9')
    plt.tight_layout()
    plt.savefig("static/pictures/skips_per_round.png")
    plt.close()


def bar_of_winners_by_starting_rank(df):
    starting_rankings = df[df["place"] == 1]["starting_rank"]
    bins = [0, 1, 2, 3, 5, 10, 20, float("inf")]
    labels = ["1", "2", "3", "4-5", "6-10", "11-20", "20+"]
    categories = pd.cut(starting_rankings, bins=bins, labels=labels, right=True)
    category_counts = categories.value_counts().sort_index()
    category_percents = category_counts / category_counts.sum() * 100

    plt.figure(figsize=(8, 8))
    plt.bar(category_counts.index, category_percents, color='royalblue', edgecolor='black', alpha=0.8)
    plt.title("Winners by Starting Rank")
    plt.xlabel("Starting Rank")
    plt.ylabel("Wins (%)")
    plt.gca().set_facecolor('#f9f9f9')
    for i, (percent, value) in enumerate(zip(category_percents, category_counts)):
        plt.text(i, percent + 0.2, f"{int(value)} wins", ha="center", fontsize=10)
    plt.tight_layout()
    plt.savefig("static/pictures/winners_by_starting_rank.png")
    plt.close()


def winners_by_rating(df):
    ratings = df[df["place"] == 1]["rating"]
    bins = range(2800, 3301, 50)
    plt.figure(figsize=(8, 8))
    plt.hist(ratings, bins=bins, color='royalblue', edgecolor='black', alpha=0.8)
    plt.title("Winners by Rating")
    plt.xticks(bins)
    plt.ylabel("Wins (%)")
    plt.gca().set_facecolor('#f9f9f9')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.savefig("static/pictures/winners_by_rating.png")
    plt.close()
    

def players_by_participation(df, limit=100):
    top_participators = df["real_name"].value_counts()
    return top_participators[:limit].to_dict()


def top_3_finishers(df):
    first = df[df["place"] == 1]["real_name"].value_counts()
    second = df[df["place"] == 2]["real_name"].value_counts()
    third = df[df["place"] == 3]["real_name"].value_counts()
    winners = pd.merge(first, second, how='outer', on="real_name", suffixes=('_1', '_2'))
    winners = pd.merge(winners, third, how='outer', on="real_name")
    winners.fillna(0, inplace=True)
    winners.reset_index(inplace=True)
    winners.rename(columns={"count_1" : '1', "count_2" : '2', "count" : '3'}, inplace=True)
    winners.sort_values(by=["1", "2", "3"], inplace=True)
    
    # Sums gold, silver, and bronze medals of the top player
    max_medals = winners.iloc[-1, 1:].sum()  
    stop = (max_medals // 10) * 10 + 11
    colors = ["gold", "silver", "brown"]
    winners.set_index("real_name").plot(kind='barh', stacked=True, color=colors, figsize=(12,20))
    plt.title("Titled Tuesday Top 3 Finishers", fontsize=20)
    plt.xticks(np.arange(0, stop, 5))
    plt.xlabel("Number of medals")
    plt.ylabel(None)
    plt.grid(axis='x', linestyle='--', color='royalblue', alpha=0.7)
    plt.gca().set_facecolor('#f9f9f9')
    plt.tight_layout()
    plt.savefig("static/pictures/top_3_finishers.png")
    plt.close()
