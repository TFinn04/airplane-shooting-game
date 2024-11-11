import pygame

# Khoi tao font
pygame.font.init()

# Dinh dang cua so
screen_width = 800
screen_height = 600

# Mau sac
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)

# Dinh dang may bay
spaceship_width = 50
spaceship_height = 60
spaceship_speed = 5

# Dinh dang dan
bullet_speed = 7
bullet_width = 5
bullet_height = 10

# Dinh dang ke dich
enemy_speed = 3
enemy_width = 50
enemy_height = 50

# Cau hinh chi so game
max_health = 100
damage_per_collision = 20
lives = 3

# Font and clock
font = pygame.font.SysFont(None, 35)
clock = pygame.time.Clock()
high_score_file = "high_score.txt"

# Load hinh anh
player_image = pygame.image.load("player.png")
enemy_image = pygame.image.load("enemy.png")
bullet_image = pygame.image.load("bullets.png")
