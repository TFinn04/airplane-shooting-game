import pygame
import random
from constants import *

class Meteor:
    def __init__(self, screen_width, screen_height):
        # Tăng tính đa dạng bằng cách sử dụng nhiều hình ảnh thiên thạch
        import os
        meteor_images = [
            image for image in [
                "Images/meteor.png",
                "Images/meteor_x.png",
                "Images/meteor_y.png"
            ] if os.path.exists(image)
        ]
        
        # Chọn ngẫu nhiên một hình ảnh
        self.image = pygame.image.load(random.choice(meteor_images)).convert_alpha()
        
        # Thay đổi kích thước ngẫu nhiên
        scale_factor = random.uniform(0.5, 2.0)  # Tỷ lệ thu phóng
        self.image = pygame.transform.scale(
            self.image, 
            (
                int(self.image.get_width() * scale_factor), 
                int(self.image.get_height() * scale_factor)
            )
        )
        
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, max(0, screen_width - self.rect.width))
        self.rect.y = -self.rect.height

        # Lưu giá trị screen_width làm thuộc tính của lớp
        self.screen_width = screen_width

        # Điều chỉnh tốc độ dựa trên kích thước thiên thạch
        self.speed_y = random.randint(3, 8) * (2.0 - scale_factor)  # Lớn chậm, nhỏ nhanh
        self.speed_x = random.choice([-1, 1]) * random.randint(1, 5)

    def move(self):
        self.rect.y += self.speed_y  # Di chuyển theo trục Y
        self.rect.x += self.speed_x  # Di chuyển theo trục X

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def off_screen(self, screen_height):
        return self.rect.y > screen_height  # Thiên thạch ra khỏi màn hình
