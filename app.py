from flask import Flask, render_template, request
import pandas as pd
from tournaments import (
    plot_num_of_players, average_score_of_winner, average_score_of_top_10,
    average_rating_of_top_10, skips_per_round, starting_ranks_of_winners,
    players_by_participation, top_3_finishers
)
from players import plot_player_ranking, analyze_player_performance
from general import slice_by_date

app = Flask(__name__)

# Load data
data = pd.read_csv("static/data.csv")

@app.route("/", methods=["GET", "POST"])
def home():
    mode = request.form.get("mode", "tournament")  # Get selected option (tournament/player)
    player_name = request.form.get("player_name", "Hikaru Nakamura")
    start_date = request.form.get("start_date", data["date"].min())
    stop_date = request.form.get("stop_date", data["date"].max())
    stats = None
    top_participators = None

    df = slice_by_date(data, start_date, stop_date)

    if mode == "tournament":
        # Generate tournament stats
        plot_num_of_players(df)
        average_score_of_winner(df)
        average_score_of_top_10(df)
        average_rating_of_top_10(df)
        skips_per_round(df)
        starting_ranks_of_winners(df)
        top_3_finishers(df)
        top_participators = players_by_participation(df)

    elif mode == "player" and player_name:
        # Generate player stats
        plot_player_ranking(df, player_name)
        stats = analyze_player_performance(df, player_name)

    return render_template("index.html", mode=mode, player_name=player_name, stats=stats,
                            top_participators=top_participators, start_date=start_date, stop_date=stop_date)

if __name__ == "__main__":
    app.run(debug=True)
