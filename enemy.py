import pygame
import os
import time
import random
from constants import *

class Enemy:
    # Thêm kẻ địch tại vị trí x,y. Status: Trạng thái kẻ địch (0: kẻ địch tự do; 1,2,3: kẻ địch thuộc đội hình 1,2,3)
    def __init__(self, enemy_x, enemy_y, status):
        self.rect = pygame.Rect(enemy_x, enemy_y, enemy_width, enemy_height)
        self.in_formation = status
        self.bullets = []
        
        # Tải animation của đạn
        self.bullet_frames = []
        self.bullet_animation_folder = "Images/enemy_bullet/"
        self.bullet_frames = sorted(
            [f for f in os.listdir(self.bullet_animation_folder) if f.endswith(".png")]
        )
        self.bullet_frame_count = len(self.bullet_frames)
        self.bullet_animation_start_time = time.time()

        self.bullet_width = bullet_width
        self.bullet_height = bullet_height
        
        # Randomly select an animation folder for the enemy itself
        self.animation_folder = f"Images/enemy_anim/enemy{random.randint(1, 4)}/"
        self.animation_frames = sorted(
            [f for f in os.listdir(self.animation_folder) if f.endswith(".png")]
        )
        self.animation_frame_count = len(self.animation_frames)
        self.animation_start_time = time.time()

    def move(self):
        # Cách kẻ địch di chuyển
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
        # Tính toán frame hiện tại dựa trên thời gian trôi qua
        elapsed_time = time.time() - self.animation_start_time
        frame_index = int(elapsed_time * 10) % self.animation_frame_count
        image_path = os.path.join(self.animation_folder, self.animation_frames[frame_index])
        self.image = pygame.image.load(image_path).convert_alpha()
        
        # Hiển thị kẻ địch
        screen.blit(self.image, (self.rect.x, self.rect.y))

        # Vẽ các viên đạn với animation
        self.animate_bullets(screen)

    def animate_bullets(self, screen):
        # Cập nhật frame đạn dựa trên thời gian
        bullet_elapsed_time = time.time() - self.bullet_animation_start_time
        bullet_frame_index = int(bullet_elapsed_time * 10) % self.bullet_frame_count
        bullet_image_path = os.path.join(self.bullet_animation_folder, self.bullet_frames[bullet_frame_index])
        bullet_image = pygame.image.load(bullet_image_path).convert_alpha()

        # Vẽ tất cả các viên đạn
        for bullet in self.bullets:
            screen.blit(bullet_image, (bullet.x, bullet.y))

    def shoot(self):
        # Tạo đạn của kẻ địch
        bullet = pygame.Rect(
            self.rect.x + enemy_width // 2 - self.bullet_width // 2,
            self.rect.y,
            self.bullet_width,
            self.bullet_height,
        )
        self.bullets.append(bullet)

    def update_bullets(self):
        # Di chuyển các viên đạn và loại bỏ những viên đạn ra ngoài màn hình
        for bullet in self.bullets:
            bullet.y += enemy_bullet_speed
        self.bullets = [
            bullet for bullet in self.bullets if bullet.y < screen_height
        ]  # Loại bỏ đạn khi chúng ra khỏi màn hình
