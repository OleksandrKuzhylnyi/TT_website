from flask import Flask, render_template, request
from sqlalchemy import create_engine, text
import pandas as pd
from tournaments import (
    plot_num_of_players, average_score_of_winner, average_score_of_top_10,
    average_rating_of_top_10, skips_per_round, bar_of_winners_by_starting_rank,
    winners_by_rating, players_by_participation, top_3_finishers
)
from players import plot_player_ranking, analyze_player_performance
from general import slice_by_date

app = Flask(__name__)

engine = create_engine("sqlite:///chess.db")

@app.route("/", methods=["GET", "POST"])
def home():
    with engine.connect() as conn:
        data = pd.read_sql("SELECT * FROM tournaments", conn)
        data['date'] = pd.to_datetime(data['date'])
        
    mode = request.form.get("mode", "tournament")  # Get selected option (tournament/player)
    player_name = request.form.get("player_name", "Hikaru Nakamura")
    player_to_compare = request.form.get("player_to_compare", "Magnus Carlsen")
    start_date = request.form.get("start_date", data["date"].min().strftime('%Y-%m-%d'))
    stop_date = request.form.get("stop_date", data["date"].max().strftime('%Y-%m-%d'))
    stats = None
    stats_to_compare = None
    top_participators = None

    df = slice_by_date(start_date, stop_date)

    if mode == "tournament":
        # Generate tournament stats
        plot_num_of_players(df)
        average_score_of_winner(df)
        average_score_of_top_10(df)
        average_rating_of_top_10(df)
        skips_per_round(df)
        bar_of_winners_by_starting_rank(df)
        winners_by_rating(df)
        top_3_finishers(df)
        top_participators = players_by_participation(df)

    elif mode == "player" and player_name:
        # Generate player stats
        plot_player_ranking(df, player_name)
        stats = analyze_player_performance(df, player_name)
        if player_to_compare:
            stats_to_compare = analyze_player_performance(df, player_to_compare)

    return render_template("index.html",
                            mode=mode,
                            player_name=player_name,
                            player_to_compare=player_to_compare,
                            stats=stats,
                            stats_to_compare=stats_to_compare,
                            top_participators=top_participators,
                            start_date=start_date,
                            stop_date=stop_date, )

if __name__ == "__main__":
    app.run(debug=True)
