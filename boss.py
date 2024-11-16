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
        self.direction = 1  # 1 for right, -1 for left
        self.bullets = []
        self.bullet_image = pygame.image.load("Images/enemy_bullet.png").convert_alpha()
        self.last_shot_time = pygame.time.get_ticks()

    def move(self):
        # Existing move method for vertical movement
        target_y = -boss_height//3
        if self.rect.y < target_y:
            self.rect.y += boss_speed  # Move down
        else:
            self.rect.y = target_y  # Stop at middle top

    def attack1(self):
        # Horizontal movement for attack1
        if self.rect.x <= 0:
            self.direction = 1
        elif self.rect.x >= screen_width - self.rect.width:
            self.direction = -1
        
        self.rect.x += boss_speed * self.direction

        # Shooting mechanism
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot_time > 300:  # Fire every 0.1 seconds
            # Bullet from left wing
            self.bullets.append(pygame.Rect(self.rect.x + self.rect.x//6, self.rect.centery - self.rect.y, self.bullet_image.get_width(), self.bullet_image.get_height()))
            # Bullet from right wing
            self.bullets.append(pygame.Rect(self.rect.right- self.rect.x//6 - self.bullet_image.get_width(), self.rect.centery - self.rect.y, self.bullet_image.get_width(), self.bullet_image.get_height()))
            self.last_shot_time = current_time

    def draw(self, screen):
        # Draw the boss image
        screen.blit(self.image, (self.rect.x, self.rect.y))
        # Draw bullets
        for bullet in self.bullets:
            screen.blit(self.bullet_image, (bullet.x, bullet.y))

    def take_damage(self, damage):
        # Reduce health by damage amount
        self.health -= damage
        return self.health <= 0  # Returns True if health is depleted

    def update_bullets(self):
        # Update bullet positions
        for bullet in self.bullets:
            bullet.y += enemy_bullet_speed
        # Remove bullets that have left the screen
        self.bullets = [bullet for bullet in self.bullets if bullet.y < screen_height]