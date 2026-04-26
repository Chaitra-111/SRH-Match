from flask import Flask, render_template
import pandas as pd
import matplotlib.pyplot as plt
import os

app = Flask(__name__)

# Dataset
data = {
    "Opponent": ["RR", "DC", "CSK", "PBKS", "LSG"],
    "SRH_Score": [229, 242, 194, 219, 156],
    "Opponent_Score": [228, 195, 184, 223, 160],
    "Result": ["Win", "Win", "Win", "Loss", "Loss"],
    "Best_Player": [
        "Abhishek Sharma",
        "Travis Head",
        "Heinrich Klaasen",
        "Shikhar Dhawan",
        "KL Rahul"
    ]
}

df = pd.DataFrame(data)

# Create static folder if not exists
if not os.path.exists("static"):
    os.makedirs("static")

# Function to generate graphs
def generate_graphs():

    # 1. SRH Scores
    plt.figure()
    plt.bar(df["Opponent"], df["SRH_Score"])
    plt.title("SRH Scores vs Opponents")
    plt.savefig("static/score.png")
    plt.close()

    # 2. Match Results
    result_counts = df["Result"].value_counts()
    plt.figure()
    plt.pie(result_counts, labels=result_counts.index, autopct='%1.1f%%')
    plt.title("Match Results")
    plt.savefig("static/result.png")
    plt.close()

    # 3. Score Comparison
    plt.figure()
    plt.plot(df["Opponent"], df["SRH_Score"], marker='o', label="SRH")
    plt.plot(df["Opponent"], df["Opponent_Score"], marker='o', label="Opponent")
    plt.legend()
    plt.title("Score Comparison")
    plt.savefig("static/comparison.png")
    plt.close()

    # 4. Best Player
    best_player = df["Best_Player"].value_counts()
    plt.figure()
    plt.bar(best_player.index, best_player.values)
    plt.xticks(rotation=30)
    plt.title("Best Player Count")
    plt.savefig("static/player.png")
    plt.close()

@app.route("/")
def home():
    generate_graphs()  # Generate charts

    avg_score = round(df["SRH_Score"].mean(), 2)
    highest = df["SRH_Score"].max()
    wins = (df["Result"] == "Win").sum()

    return render_template("index.html",
                           avg_score=avg_score,
                           highest=highest,
                           wins=wins)

if __name__ == "__main__":
    app.run(debug=True)