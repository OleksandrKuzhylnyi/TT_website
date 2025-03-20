from flask import Flask, render_template, request
from sqlalchemy import create_engine, text
import pandas as pd
from tournaments import (
    plot_num_of_players, average_score_of_winner, average_score_of_top_10,
    average_rating_of_top_10, skips_per_round, bar_of_winners_by_starting_rank,
    winners_by_rating, players_by_participation, top_3_finishers
)
from players import (
    plot_player_ranking, analyze_player_performance, analyze_perfomance_by_rounds
)
from general import slice_by_date

app = Flask(__name__)

engine = create_engine("sqlite:///chess.db")

@app.route("/", methods=["GET", "POST"])
def home():
    with engine.connect() as conn:
        data = pd.read_sql("SELECT * FROM tournaments", conn)
        data['date'] = pd.to_datetime(data['date'])
        
    mode = request.form.get("mode", "tournament")  # Get selected option (tournament/player)
    start_date = request.form.get("start_date", data["date"].min().strftime('%Y-%m-%d'))
    stop_date = request.form.get("stop_date", data["date"].max().strftime('%Y-%m-%d'))
    selected_rounds = request.form.getlist("rounds", type=int)
    player_name = request.form.get("player_name", "Hikaru Nakamura")
    stats = None
    rounds_stats = None
    top_participators = None
    players = []
    stats_list = []
    players_raw = request.form.get("players", "")

    if start_date or stop_date:
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
        rounds_stats = analyze_perfomance_by_rounds(df, player_name)

    elif mode == "comparison":
        players = [p.strip() for p in players_raw.split("\n") if p.strip()]
        for player in players:
            stats_list.append(analyze_player_performance(df, player))

    return render_template(
        "index.html",
        mode=mode,
        start_date=start_date,
        stop_date=stop_date,
        selected_rounds=selected_rounds,
        player_name=player_name,
        stats=stats,
        players=players,
        stats_list=stats_list,
        rounds_stats=rounds_stats,
        top_participators=top_participators,
    )

if __name__ == "__main__":
    app.run(debug=True)
