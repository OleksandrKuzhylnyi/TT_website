from flask import Flask, render_template, request, redirect, url_for
from sqlalchemy import create_engine
import pandas as pd
from tournaments import (
    num_of_players, average_score_of_winner, average_score_of_top_10,
    average_rating_of_top_10, skips_per_round, winners_by_starting_rank,
    winners_by_rating, players_by_participation, top_3_finishers
)
from players import (
    plot_player_ranking, analyze_player_performance,
    analyze_performance_by_rounds, analyze_opponents
)
from general import slice_by_date

app = Flask(__name__)

engine = create_engine("sqlite:///chess.db")
with engine.connect() as conn:
    DATA = pd.read_sql("SELECT * FROM tournaments", conn)
    DATA["date"] = pd.to_datetime(DATA["date"])

MIN_DATE = DATA["date"].min().strftime('%Y-%m-%d')
MAX_DATE = DATA["date"].max().strftime('%Y-%m-%d')
    

@app.route("/")
def index():
    return redirect(url_for("tournaments"))

@app.route("/tournaments", methods=["GET", "POST"])
def tournaments():
    start_date = request.form.get("start_date", MIN_DATE)
    stop_date = request.form.get("stop_date", MAX_DATE)

    df = slice_by_date(DATA, start_date, stop_date)

    num_of_players(df)
    average_score_of_winner(df)
    average_score_of_top_10(df)
    average_rating_of_top_10(df)
    skips_per_round(df)
    winners_by_starting_rank(df)
    winners_by_rating(df)
    top_3_finishers(df)
    top_participators = players_by_participation(df)

    return render_template(
        "tournaments.html",
        current_route="tournaments",
        start_date=start_date,
        stop_date=stop_date,
        top_participators=top_participators
    )


@app.route("/player", methods=["GET", "POST"])
def player():
    start_date = request.form.get("start_date", MIN_DATE)
    stop_date = request.form.get("stop_date", MAX_DATE)

    df = slice_by_date(DATA, start_date, stop_date)

    player_name = request.form.get("player_name", "Hikaru Nakamura")

    stats = analyze_player_performance(df, player_name)
    rounds_stats = analyze_performance_by_rounds(df, player_name)
    opponents = analyze_opponents(df, player_name)
    plot_player_ranking(df, player_name)

    return render_template(
        "player.html",
        current_route="player",
        start_date=start_date,
        stop_date=stop_date,
        player_name=player_name,
        stats=stats,
        rounds_stats=rounds_stats,
        opponents=opponents,
    )


@app.route("/comparison", methods=["GET", "POST"])
def comparison():
    start_date = request.form.get("start_date", MIN_DATE)
    stop_date = request.form.get("stop_date", MAX_DATE)

    df = slice_by_date(DATA, start_date, stop_date)

    players = []
    stats_list = []
    players_raw = request.form.get("players", "")

    players = [p.strip() for p in players_raw.split("\n") if p.strip()]
    for player in players:
        stats_list.append(analyze_player_performance(df, player))

    return render_template(
        "comparison.html",
        current_route="comparison",
        start_date=start_date,
        stop_date=stop_date,
        players=players,
        stats_list=stats_list
    )


if __name__ == "__main__":
    app.run(debug=True)
