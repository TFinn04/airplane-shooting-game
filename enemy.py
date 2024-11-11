import pygame
import random
from constants import *


class Enemy:
    def __init__(self):
        # Initialize enemy position at a random horizontal location above the screen
        self.rect = pygame.Rect(
            random.randint(0, screen_width - enemy_width),
            -enemy_height,
            enemy_width,
            enemy_height,
        )
        # Load enemy image
        self.image = pygame.image.load("enemy.png").convert_alpha()

    def move(self):
        # Move the enemy downwards
        self.rect.y += enemy_speed

    def draw(self, screen):
        # Draw the enemy image
        screen.blit(self.image, (self.rect.x, self.rect.y))
