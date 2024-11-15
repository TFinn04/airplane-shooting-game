import pygame
from constants import *


class Player:
    def __init__(self, spaceship_data, screen_width, screen_height):
        # Đặt các thuộc tính từ dữ liệu máy bay
        self.x = screen_width // 2
        self.y = screen_height - spaceship_height - 10
        self.speed = spaceship_data["speed"]
        self.health = spaceship_data["hp"]
        self.max_health = spaceship_data["hp"]
        self.damage = spaceship_data["damage"]
        self.lives = lives
        self.shield = 0  # Ban đầu không có lá chắn
        self.can_shoot = True

        # Tải hình ảnh của người chơi
        self.image = pygame.image.load(spaceship_data["image"]).convert_alpha()
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        
        self.bullets = []

        # Khởi tạo thuộc tính rect để kiểm tra va chạm
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

        # Tải hình ảnh của đạn
        self.bullet_image = pygame.image.load("Images/bullets.png").convert_alpha()
        self.bullet_width = self.bullet_image.get_width()
        self.bullet_height = self.bullet_image.get_height()

        # Giới hạn màn hình
        self.screen_width = screen_width
        self.screen_height = screen_height

    def move(self, keys):
        # Di chuyển người chơi dựa trên các phím nhấn, cập nhật vị trí và rect
        if keys[pygame.K_LEFT] and self.x > 0:
            self.x -= self.speed
        if keys[pygame.K_RIGHT] and self.x < self.screen_width - self.width:
            self.x += self.speed
        if keys[pygame.K_UP] and self.y > 0:
            self.y -= self.speed
        if keys[pygame.K_DOWN] and self.y < self.screen_height - self.height:
            self.y += self.speed

        # Cập nhật vị trí rect sau khi di chuyển
        self.rect.topleft = (self.x, self.y)

    def shoot(self):
        if self.can_shoot:
            bullet = pygame.Rect(
                self.x + self.width // 2 - self.bullet_width // 2,
                self.y,
                self.bullet_width,
                self.bullet_height,
            )
            self.bullets.append(bullet)
            self.can_shoot = False  # Người chơi chỉ có thể bắn lại sau khi nhả nút

    def draw(self, screen):
        # Vẽ hình ảnh của người chơi trên màn hình
        screen.blit(self.image, (self.x, self.y))

        # Vẽ các viên đạn
        for bullet in self.bullets:
            screen.blit(self.bullet_image, (bullet.x, bullet.y))

        # Vẽ thanh máu (màu xám nếu lá chắn đang hoạt động, màu xanh nếu không)
        health_bar_color = (169, 169, 169) if self.shield > 0 else green
        pygame.draw.rect(screen, health_bar_color, (10, 50, self.health * 2, 20))

    def update_bullets(self):
        # Di chuyển các viên đạn và loại bỏ những viên đạn ra ngoài màn hình
        for bullet in self.bullets:
            bullet.y -= bullet_speed
        self.bullets = [bullet for bullet in self.bullets if bullet.y > 0]

    def lose_health(self):
        # Lá chắn hấp thụ sát thương trước, nếu đang hoạt động
        if self.shield > 0:
            self.shield -= damage_per_collision
            if self.shield < 0:
                self.health += self.shield  # Sát thương dư sẽ chuyển sang máu
                self.shield = 0  # Lá chắn bị phá hủy
        else:
            self.health -= damage_per_collision

        # Kiểm tra nếu máu bị cạn, xử lý giảm số mạng
        if self.health <= 0:
            self.lives -= 1
            self.health = max_health
            if self.lives <= 0:
                return True  # Kết thúc trò chơi (không còn mạng)
        return False  # Người chơi vẫn còn sống
