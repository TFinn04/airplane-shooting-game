import pygame
import random
from constants import *  # Import các hằng số từ constants.py


class DropItem:
    def __init__(self, screen_width, screen_height):
        # Khởi tạo vị trí và kích thước của vật phẩm
        self.rect = pygame.Rect(
            random.randint(0, screen_width - 50),  # Vị trí X ngẫu nhiên
            -50,  # Bắt đầu từ trên màn hình
            50,  # Kích thước vật phẩm
            50,
        )
        # Chọn ngẫu nhiên một trong các hiệu ứng của vật phẩm
        self.effect = random.choice(["regen", "shield", "destroy_enemies"])

        # Gán hình ảnh khác nhau dựa trên hiệu ứng
        if self.effect == "regen":
            self.image = pygame.image.load("Images/regen_item.png").convert_alpha()
        elif self.effect == "shield":
            self.image = pygame.image.load("Images/shield_item.png").convert_alpha()
        elif self.effect == "destroy_enemies":
            self.image = pygame.image.load("Images/destroy_item.png").convert_alpha()

    def move(self):
        # Di chuyển vật phẩm xuống
        self.rect.y += 3  # Tốc độ rơi (có thể điều chỉnh nếu cần)

    def draw(self, screen):
        # Vẽ vật phẩm lên màn hình
        screen.blit(self.image, (self.rect.x, self.rect.y))

    def apply_effect(self, player, enemies):
        """Áp dụng hiệu ứng của vật phẩm cho người chơi hoặc kẻ thù."""
        if self.effect == "regen":
            # Áp dụng hiệu ứng hồi phục (hồi máu cho người chơi)
            health_to_regen = max_health * regen_percentage  # Tính toán lượng hồi máu
            player.health = min(
                player.health + health_to_regen, max_health
            )  # Đảm bảo không vượt quá sức khỏe tối đa

        elif self.effect == "shield":
            # Áp dụng hiệu ứng khiên (cung cấp khiên cho người chơi)
            player.shield = shield_amount  # Cấp khiên theo lượng đã định sẵn

        elif self.effect == "destroy_enemies":
            # Hủy tất cả kẻ thù trên màn hình
            enemies.clear()  # Xóa tất cả kẻ thù khỏi màn hình
