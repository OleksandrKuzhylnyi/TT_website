from flask import Flask, render_template, request
import pandas as pd
import os
import matplotlib.pyplot as plt
from chess import get_data, plot_player_ranking  # Import your functions

app = Flask(__name__)

# Load data once at startup
df = get_data()

@app.route("/", methods=["GET", "POST"])
def home():
    player = "Hikaru Nakamura"  # Default player

    if request.method == "POST":
        player = request.form["player_name"]  # Get player name from form input

    plot_player_ranking(df, player)  # Generate ranking plot
    return render_template("index.html", player=player)

if __name__ == "__main__":
    app.run(debug=True)
