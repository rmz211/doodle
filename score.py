import os

class ScoreManager:
    def __init__(self, filepath="data/scores.txt"):
        self.filepath = filepath
        if not os.path.exists(filepath):
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            with open(filepath, "w") as f:
                f.write("0\n")

    def get_high_score(self):
        try:
            with open(self.filepath, "r") as f:
                return int(f.readline().strip())
        except (ValueError, FileNotFoundError):
            return 0

    def save_score(self, score):
        high_score = self.get_high_score()
        if score > high_score:
            with open(self.filepath, "w") as f:
                f.write(str(score))
