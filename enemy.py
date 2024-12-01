import pygame
import os
import time
import random
from constants import *


class Enemy:
    # Thêm kẻ địch tại vị trí x,y. Status: Trạng thái kẻ địch (0: kẻ địch tự do; 1,2,3: kẻ địch thuộc đội ình 1,2,3)
    def __init__(self, enemy_x, enemy_y, status):
        self.rect = pygame.Rect(enemy_x, enemy_y, enemy_width, enemy_height)
        self.in_formation = status
        # Load enemy image
        self.image = pygame.image.load("Images/enemy.png").convert_alpha()
        self.bullets = []
        self.bullet_image = pygame.image.load(
            "Images/enemy_bullet.png"
        ).convert_alpha()  # Ensure this path is correct
        self.bullet_width = self.bullet_image.get_width()
        self.bullet_height = self.bullet_image.get_height()
        
        # Randomly select an animation folder
        self.animation_folder = f"Images/enemy_anim/enemy{random.randint(1, 4)}/"
        self.animation_frames = sorted(
            [f for f in os.listdir(self.animation_folder) if f.endswith(".png")]
        )
        self.animation_frame_count = len(self.animation_frames)
        self.animation_start_time = time.time()

    def move(self):
        # cách kẻ địch di chuyển
        if self.in_formation == 0 or self.in_formation == 1:
            self.rect.y += enemy_speed
        if self.in_formation == 2:
            self.rect.x += enemy_speed
            self.rect.y += enemy_speed // 1.75
        if self.in_formation == -2:
            self.rect.x -= enemy_speed
            self.rect.y += enemy_speed // 1.75
        if self.in_formation == 3:
            self.rect.x += enemy_speed
        if self.in_formation == -3:
            self.rect.x -= enemy_speed

    def draw(self, screen):
        # Calculate current frame based on elapsed time
        elapsed_time = time.time() - self.animation_start_time
        frame_index = int(elapsed_time * 10) % self.animation_frame_count
        image_path = os.path.join(self.animation_folder, self.animation_frames[frame_index])
        self.image = pygame.image.load(image_path).convert_alpha()
        # Hiển thị kẻ địch
        screen.blit(self.image, (self.rect.x, self.rect.y))
        for bullet in self.bullets:
            screen.blit(self.bullet_image, (bullet.x, bullet.y))

    def shoot(self):

        bullet = pygame.Rect(
            self.rect.x + enemy_width // 2 - self.bullet_width // 2,
            self.rect.y,
            self.bullet_width,
            self.bullet_height,
        )
        self.bullets.append(bullet)

    def update_bullets(self):
        for bullet in self.bullets:
            bullet.y += enemy_bullet_speed
        self.bullets = [
            bullet for bullet in self.bullets if bullet.y > 0
        ]  # Loại bỏ đạn bay hết hành trình
