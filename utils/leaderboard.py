# utils/leaderboard.py
import json
import os

SCORE_FILE = os.path.join("data", "scores.json")

def load_scores():
    if not os.path.exists(SCORE_FILE):
        return []
    with open(SCORE_FILE, "r") as f:
        try:
            return json.load(f)
        except:
            return []

def save_score(topic, score, total):
    scores = load_scores()
    # Add new score
    scores.append({"topic": topic, "score": f"{score}/{total}"})
    
    # Keep only top 10 recent
    scores = scores[-10:] 
    
    os.makedirs("data", exist_ok=True)
    with open(SCORE_FILE, "w") as f:
        json.dump(scores, f)
