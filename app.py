from flask import Flask, render_template, request, redirect, url_for, jsonify
import pandas as pd
from sqlalchemy import create_engine

from tournaments import (
    plot_num_of_players, plot_average_score_of_top_10, plot_average_rating_of_top_10,
    plot_skips_per_round, plot_winners_by_starting_rank, plot_winners_by_rating,
    players_by_participation, plot_top_3_finishers
)
from players import (
    plot_player_ranking, analyze_performance,
    analyze_performance_by_rounds, get_common_opponents, head_to_head,
)
from general import slice_by_date

app = Flask(__name__)

engine = create_engine("sqlite:///chess.db")
with engine.connect() as conn:
    DATA = pd.read_sql("SELECT * FROM tournaments", conn)
    DATA["date"] = pd.to_datetime(DATA["date"])

MIN_DATE = DATA["date"].min().strftime('%Y-%m-%d')
MAX_DATE = DATA["date"].max().strftime('%Y-%m-%d')
PLAYER_NAMES = DATA.sort_values(["rating"], ascending=False).real_name.dropna().unique()

@app.route("/")
def index():
    return redirect(url_for("tournaments"))

@app.route("/tournaments", methods=["GET", "POST"])
def tournaments():
    start_date = request.form.get("start_date", MIN_DATE)
    stop_date = request.form.get("stop_date", MAX_DATE)

    df = slice_by_date(DATA, start_date, stop_date)

    plot_num_of_players(df)
    plot_average_score_of_top_10(df)
    plot_average_rating_of_top_10(df)
    plot_skips_per_round(df)
    plot_winners_by_starting_rank(df)
    plot_winners_by_rating(df)
    plot_top_3_finishers(df)
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
    player_name = request.form.get("player_name", "Hikaru Nakamura").strip()
    
    rounds_stats = analyze_performance_by_rounds(df, player_name)
    white_opponents, black_opponents, opponents = get_common_opponents(df, player_name)
    white_stats, black_stats, stats = analyze_performance(df, player_name)
    plot_player_ranking(df, player_name)

    return render_template(
        "player.html",
        current_route="player",
        start_date=start_date,
        stop_date=stop_date,
        player_name=player_name,
        stats=stats,
        rounds_stats=rounds_stats,
        white_opponents=white_opponents,
        black_opponents=black_opponents,
        opponents=opponents,
        white_stats=white_stats,
        black_stats=black_stats
    )


@app.route("/comparison", methods=["GET", "POST"])
def comparison():
    start_date = request.form.get("start_date", MIN_DATE)
    stop_date = request.form.get("stop_date", MAX_DATE)

    df = slice_by_date(DATA, start_date, stop_date)

    players = []
    stats_list = []
    players_raw = request.form.get("players", "Hikaru Nakamura\nMagnus Carlsen")

    players = [p.strip() for p in players_raw.split("\n") if p.strip()]
    for player in players:
        stats_list.append(analyze_performance(df, player)[2])

    white_results, black_results, results, white_total, black_total, total = head_to_head(df, players)

    return render_template(
        "comparison.html",
        current_route="comparison",
        start_date=start_date,
        stop_date=stop_date,
        players=players,
        stats_list=stats_list,
        white_results=white_results,
        results=results,
        white_total=white_total,
        black_total=black_total,
        total=total,
    )


@app.route('/autocomplete', methods=["GET"])
def autocomplete():
    query = request.args.get('query', '').lower()
    suggestions = [name for name in PLAYER_NAMES if query in name.lower()]
    return jsonify(suggestions[:10])


if __name__ == "__main__":
    app.run(debug=True)
