import pygame
from constants import *

class Boss:
    def __init__(self):
        # Initialize boss position at the middle top of the screen
        self.rect = pygame.Rect(
            (screen_width - boss_width) // 2, 
            -boss_height,  # Start just above the screen
            boss_width,
            boss_height,
        )
        self.health = boss_health
        self.image = pygame.image.load("Images/boss.png").convert_alpha()

    def move(self):
        # Move the boss downwards slowly
        target_y = -boss_height//3# Middle top of the screen
        if self.rect.y < target_y:
            self.rect.y += boss_speed  # Move down
        else:
            self.rect.y = target_y  # Stop at middle top

    def draw(self, screen):
        # Draw the boss image
        screen.blit(self.image, (self.rect.x, self.rect.y))

    def take_damage(self, damage):
        # Reduce health by damage amount
        self.health -= damage
        return self.health <= 0  # Returns True if health is depleted
