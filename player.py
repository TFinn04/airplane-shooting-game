import pygame
import os
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

        # Load ảnh đạn tàu bay
        self.frames = []
        image_folder = spaceship_data["image_folder"]
        for filename in sorted(os.listdir(image_folder)):  # Đảm bảo thứ tự frame
            if filename.endswith(".png"):
                frame = pygame.image.load(os.path.join(image_folder, filename)).convert_alpha()
                self.frames.append(frame)
        self.current_frame = 0  # Frame hiện tại
        self.animation_speed = 5  # Tốc độ chuyển frame
        self.frame_counter = 0
        
        self.width = self.frames[0].get_width()
        self.height = self.frames[0].get_height()
        
        self.bullets = []

        # Khởi tạo thuộc tính rect để kiểm tra va chạm
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

        # Load animation của đạn cho máy bay cụ thể
        self.bullet_frames = []
        bullet_anim_folder = spaceship_data["bullet_folder"]
        for filename in sorted(os.listdir(bullet_anim_folder)):  # Đảm bảo thứ tự frame
            if filename.endswith(".png"):
                bullet_frame = pygame.image.load(os.path.join(bullet_anim_folder, filename)).convert_alpha()
                self.bullet_frames.append(bullet_frame)
        self.current_bullet_frame = 0
        self.bullet_animation_speed = 5  # Tốc độ animation của đạn
        self.bullet_frame_counter = 0
        
        self.bullet_width = self.bullet_frames[0].get_width()
        self.bullet_height = self.bullet_frames[0].get_height()

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

    def animate(self):
        # Điều chỉnh khung hình mỗi khi bộ đếm đạt đến ngưỡng tốc độ
        self.frame_counter += 1
        if self.frame_counter >= self.animation_speed:
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.frame_counter = 0
            
        # Cập nhật animation của đạn
        self.bullet_frame_counter += 1
        if self.bullet_frame_counter >= self.bullet_animation_speed:
            self.current_bullet_frame = (self.current_bullet_frame + 1) % len(self.bullet_frames)
            self.bullet_frame_counter = 0

    def shoot(self):
        if self.can_shoot:
            bullet = pygame.Rect(
                self.x + self.width // 2 - self.bullet_width // 2,
                self.y,
                self.bullet_width,
                self.bullet_height,
            )
            self.bullets.append(bullet)
            self.can_shoot = False # Người chơi chỉ có thể bắn lại sau khi nhả nút

    def draw(self, screen):
        # Gọi animate để chuyển frame
        self.animate()
        screen.blit(self.frames[self.current_frame], (self.x, self.y))

        # Vẽ các viên đạn với animation
        for bullet in self.bullets:
            screen.blit(self.bullet_frames[self.current_bullet_frame], (bullet.x, bullet.y))

        # Vẽ thanh máu (màu xám nếu lá chắn đang hoạt động, màu xanh nếu không)
        pygame.draw.rect(screen, white, (8, 48, self.max_health * 2 + 4, 24), 2)
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
    
    def lose_health_dot(self):
        # Lá chắn hấp thụ sát thương trước, nếu đang hoạt động
        if self.shield > 0:
            self.shield -= damage_per_collision
            if self.shield < 0:
                self.health += self.shield  # Sát thương dư sẽ chuyển sang máu
                self.shield = 0  # Lá chắn bị phá hủy
        else:
            self.health -= damage_over_time

        # Kiểm tra nếu máu bị cạn, xử lý giảm số mạng
        if self.health <= 0:
            self.lives -= 1
            self.health = max_health
            if self.lives <= 0:
                return True  # Kết thúc trò chơi (không còn mạng)
        return False  # Người chơi vẫn còn sống