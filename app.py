from flask import Flask, render_template, request
import pandas as pd
from chess import *

app = Flask(__name__)

# Load dataset
df = get_data()

@app.route("/", methods=["GET", "POST"])
def home():
    player = "Hikaru Nakamura"  # Default player
    feature = "ranking"  # Default feature
    stats = None
    max_players = None
    top_participators = None

    if request.method == "POST":
        feature = request.form.get("feature", "ranking")  # Get feature selection

        if feature in ["ranking", "performance"]:
            player = request.form.get("player_name", player)  # Get player name safely

            if feature == "ranking":
                plot_player_ranking(df, player)

            elif feature == "performance":
                stats = analyze_player_performance(df, player)
                if "error" in stats:
                    stats = None  # Handle player not found

        elif feature == "tournament":
            plot_num_of_players(df)
            max_players = {
                "early": df[df["time"] == "E"].groupby("date")["Number"].max().to_dict(),
                "late": df[df["time"] == "L"].groupby("date")["Number"].max().to_dict(),
            }

        elif feature == "participation":
            top_participators = players_by_participation(df)

    return render_template("index.html", player=player, stats=stats, feature=feature,
                            max_players=max_players, top_participators=top_participators)

if __name__ == "__main__":
    app.run(debug=True)
