import pygame
import random
from constants import *


class Enemy:
    def __init__(self):
        # Initialize enemy position at a random horizontal location above the screen
        self.rect = pygame.Rect(random.randint(0, screen_width - enemy_width),-enemy_height,enemy_width,enemy_height)
        
        # Load enemy image
        self.image = pygame.image.load("enemy.png").convert_alpha()
        self.bullets =[]
        self.bullet_image = pygame.image.load("enemy_bullet.png").convert_alpha()  # Ensure this path is correct
        self.bullet_width = self.bullet_image.get_width()
        self.bullet_height = self.bullet_image.get_height()

    def move(self):
        # Move the enemy downwards
        self.rect.y += enemy_speed

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

