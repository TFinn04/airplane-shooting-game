import json


# Tải cấu hình từ file config.json
def load_config():
    with open("config.json", "r") as file:
        return json.load(file)


# Tải cấu hình trò chơi từ config.json
config = load_config()

# Cấu hình trò chơi (được di chuyển từ các hằng số)
screen_width = config["screen_width"]  # Chiều rộng màn hình
screen_height = config["screen_height"]  # Chiều cao màn hình

# Các màu sắc (hằng số, không cần tải từ cấu hình)
black = (0, 0, 0)  # Màu đen
white = (255, 255, 255)  # Màu trắng
red = (255, 0, 0)  # Màu đỏ
green = (0, 255, 0)  # Màu xanh lá
yellow = (255, 223, 0)
light_blue = (173, 216, 230)
dark_blue = (10, 10, 50)
neon_blue = (0, 255, 255)

# Thống kê của người chơi
spaceship_width = config["spaceship_width"]  # Chiều rộng tàu không gian
spaceship_height = config["spaceship_height"]  # Chiều cao tàu không gian
spaceship_speed = config["spaceship_speed"]  # Tốc độ di chuyển của tàu
max_health = config["max_health"]  # Sức khỏe tối đa của người chơi
lives = config["lives"]  # Số mạng của người chơi

# Thống kê của đạn
bullet_speed = config["bullet_speed"]  # Tốc độ di chuyển của đạn
bullet_width = config["bullet_width"]  # Chiều rộng của đạn
bullet_height = config["bullet_height"]  # Chiều cao của đạn

# Thống kê của kẻ thù
enemy_width = config["enemy_width"]  # Chiều rộng của kẻ thù
enemy_height = config["enemy_height"]  # Chiều cao của kẻ thù
enemy_speed = config["enemy_speed"]  # Tốc độ di chuyển của kẻ thù
enemy_bullet_speed = config["enemy_bullet_speed"]  # Tốc độ đạn của kẻ thù

# Sát thương mỗi lần va chạm
damage_per_collision = config["damage_per_collision"]  # Sát thương khi va chạm

# Các hằng số liên quan đến vật phẩm
item_drop_interval = config[
    "item_drop_interval"
]  # Khoảng thời gian giữa các lần thả vật phẩm
shield_amount = config["shield_amount"]  # Số lượng khiên mà vật phẩm cung cấp
max_shield = config["max_shield"]  # Số lượng khiên tối đa
regen_amount = config["regen_amount"]  # Số lượng hồi phục khi vật phẩm hồi máu

#thống kê boss
boss_health = config["boss_health"]
boss_width = config["boss_width"]
boss_height = config["boss_height"]
boss_speed = config["boss_speed"]