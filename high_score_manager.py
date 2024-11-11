import os


class HighScoreManager:
    def __init__(self, filename):
        self.filename = filename
        self.high_score = self.load_high_score()

    def load_high_score(self):
        # Load diem ki luc tu file, hoac tao file diem ki luc neu khong ton tai
        if not os.path.exists(self.filename):
            with open(self.filename, "w") as file:
                file.write("0")
        with open(self.filename, "r") as file:
            return int(file.read().strip())

    def save_high_score(self, score):
        # Luu dien vao file
        with open(self.filename, "w") as file:
            file.write(str(score))

    def reset_high_score(self):
        # Reset diem cao
        self.save_high_score(0)
        self.high_score = 0
