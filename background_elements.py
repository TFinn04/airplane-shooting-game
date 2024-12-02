import pygame
import random
from constants import *

class Planets:
    def __init__(self, screen_width, screen_height):
        
        import os
        planet_images = [
            image for image in [
                "Images/planets/A00.png",
                "Images/planets/A01.png",
                "Images/planets/M00.png",
                "Images/planets/M01.png",
                "Images/planets/M02.png",
                "Images/planets/J00.png",
                "Images/planets/J01.png",
                "Images/planets/J02.png",
                "Images/planets/G00.png",
                "Images/planets/M06.png",
                "Images/planets/L00.png"
            ] if os.path.exists(image)
        ]
        
        # Chọn ngẫu nhiên một hình ảnh
        self.image = pygame.image.load(random.choice(planet_images)).convert_alpha()
        
        # Thay đổi kích thước ngẫu nhiên
        scale_factor = random.uniform(1.0, 4.0)  # Tỷ lệ thu phóng
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

       
        

    def move(self):
        self.rect.y += enemy_speed-0.5  # Di chuyển theo trục Y
    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def off_screen(self, screen_height):
        return self.rect.y > screen_height  # Thiên thạch ra khỏi màn hình
