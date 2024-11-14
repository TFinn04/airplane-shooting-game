import os


class HighScoreManager:
    def __init__(self, filename):
        self.filename = filename
        self.high_score = self.load_high_score()

    def load_high_score(self):
        # Load điểm kỷ lục từ file hoặc tạo file nếu không tồn tại
        if not os.path.exists(self.filename):
            with open(self.filename, "w") as file:
                file.write("0")
        with open(self.filename, "r") as file:
            return int(file.read().strip())

    def save_high_score(self, score):
        # Lưu điểm
        with open(self.filename, "w") as file:
            file.write(str(score))

    def reset_high_score(self):
        # Reset
        self.save_high_score(0)
        self.high_score = 0
