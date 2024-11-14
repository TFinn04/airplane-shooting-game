import pygame
from constants import *


class Player:
    def __init__(self, screen_width, screen_height):
        self.x = screen_width // 2
        self.y = screen_height - spaceship_height - 10
        self.speed = spaceship_speed
        self.bullets = []
        self.health = max_health
        self.lives = lives
        self.can_shoot = True

        # Load hình ảnh người chơi
        self.image = pygame.image.load("player.png").convert_alpha()
        self.width = self.image.get_width()
        self.height = self.image.get_height()

        # Load hình ảnh đạn
        self.bullet_image = pygame.image.load("bullets.png").convert_alpha()
        self.bullet_width = self.bullet_image.get_width()
        self.bullet_height = self.bullet_image.get_height()

        self.screen_width = screen_width
        self.screen_height = screen_height

    def move(self, keys):
        # Di chuyển nếu phím tương ứng được bấm và đang không ở rìa màn hình
        if keys[pygame.K_LEFT] and self.x > 0:
            self.x -= self.speed
        if keys[pygame.K_RIGHT] and self.x < self.screen_width - self.width:
            self.x += self.speed
        if keys[pygame.K_UP] and self.y > 0:
            self.y -= self.speed
        if keys[pygame.K_DOWN] and self.y < self.screen_height - self.height:
            self.y += self.speed

    def shoot(self):
        if self.can_shoot:
            bullet = pygame.Rect(
                self.x + self.width // 2 - self.bullet_width // 2,
                self.y,
                self.bullet_width,
                self.bullet_height,
            )
            self.bullets.append(bullet)
            self.can_shoot = False  # Chỉ được bắn tiếp khi thả nút

    def draw(self, screen):
        # Vẽ hình ảnh người chơi lên màn hình
        screen.blit(self.image, (self.x, self.y))

        # Vẽ hình ảnh của đạn
        for bullet in self.bullets:
            screen.blit(self.bullet_image, (bullet.x, bullet.y))

        # Hiện thanh máu
        pygame.draw.rect(screen, green, (10, 50, self.health * 2, 20))

    def update_bullets(self):
        for bullet in self.bullets:
            bullet.y -= bullet_speed
        self.bullets = [
            bullet for bullet in self.bullets if bullet.y > 0
        ]  # Loại bỏ đạn nếu đã đi hết hành trình

    def lose_health(self):
        self.health -= damage_per_collision
        if self.health <= 0:
            self.lives -= 1
            self.health = max_health
            if self.lives <= 0:
                return True  # Người chơi hết mạng
        return False  # Người chơi vẫn còn sống
