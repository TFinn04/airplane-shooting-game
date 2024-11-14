import json


# Load configuration from config.json
def load_config():
    with open("config.json", "r") as file:
        return json.load(file)


# Load the configuration
config = load_config()

# Game configuration (moved from constants)
screen_width = config["screen_width"]
screen_height = config["screen_height"]

# Colors (constants, no need to load from config)
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)

# Player statistics
spaceship_width = config["spaceship_width"]
spaceship_height = config["spaceship_height"]
spaceship_speed = config["spaceship_speed"]
max_health = config["max_health"]
lives = config["lives"]

# Bullet statistics
bullet_speed = config["bullet_speed"]
bullet_width = config["bullet_width"]
bullet_height = config["bullet_height"]

# Enemy statistics
enemy_width = config["enemy_width"]
enemy_height = config["enemy_height"]
enemy_speed = config["enemy_speed"]
enemy_bullet_speed = config["enemy_bullet_speed"]

# Damage per collision
damage_per_collision = config["damage_per_collision"]
