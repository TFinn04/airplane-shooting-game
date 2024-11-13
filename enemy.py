import pygame
import random
from constants import *


class Enemy:
    # Thêm kẻ địch tại vị trí x,y. Status: Trạng thái kẻ địch (0: kẻ địch tự do; 1,2,3: kẻ địch thuộc đội ình 1,2,3)
    def __init__(self,enemy_x,enemy_y,status):
        self.rect = pygame.Rect(enemy_x,enemy_y,enemy_width,enemy_height)
        self.in_formation=status
        # Load enemy image
        self.image = pygame.image.load("enemy.png").convert_alpha()
        self.bullets =[]
        self.bullet_image = pygame.image.load("enemy_bullet.png").convert_alpha()  # Ensure this path is correct
        self.bullet_width = self.bullet_image.get_width()
        self.bullet_height = self.bullet_image.get_height()

    def move(self):
        # cách kẻ địch di chuyển
        if self.in_formation == 0 or self.in_formation == 1:
            self.rect.y += enemy_speed
        if self.in_formation == 2:
            self.rect.x += enemy_speed
            self.rect.y += enemy_speed//1.75
        if self.in_formation == -2:
            self.rect.x -= enemy_speed
            self.rect.y += enemy_speed//1.75
        if self.in_formation == 3:
            self.rect.x += enemy_speed
        if self.in_formation == -3:
            self.rect.x -= enemy_speed

    def draw(self, screen):
        # Draw the enemy image
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
            bullet.y += bullet_speed
        self.bullets = [
            bullet for bullet in self.bullets if bullet.y > 0
        ]  # Remove off-screen bullets        

