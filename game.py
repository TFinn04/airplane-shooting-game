import pygame
import random
from drop_item import DropItem
from player import Player
from enemy import Enemy
from high_score_manager import HighScoreManager
from constants import *  # Nhập các hằng số từ file constants


class Game:
    def __init__(self):
        # Khởi tạo trình quản lý điểm cao và hình nền
        self.high_score_manager = HighScoreManager("high_score.txt")
        self.background_image = pygame.image.load("Images/background.png").convert()

        # Cấu hình khoảng thời gian sinh kẻ địch và rơi vật phẩm
        self.last_spawn_time = pygame.time.get_ticks()
        self.spawn_delay = config["enemy_spawn_delay"]
        self.item_drop_interval = config["item_drop_interval"]
        self.last_item_drop_time = pygame.time.get_ticks()

        # Khởi tạo danh sách vật phẩm và kẻ địch
        self.items = []  # Danh sách để lưu trữ các vật phẩm đang hoạt động
        self.enemies = []  # Danh sách để lưu trữ các kẻ địch đang hoạt động

    def draw_text(self, text, x, y, screen, color=white):
        font = pygame.font.SysFont("Arial", 35)
        screen_text = font.render(text, True, color)
        screen.blit(screen_text, (x, y))

    def apply_item_effect(self, player, item):
        """Áp dụng hiệu ứng của vật phẩm khi người chơi thu thập nó."""
        if item.effect == "regen":
            player.health = min(player.health + regen_amount, max_health)
        elif item.effect == "shield":
            player.shield = min(player.shield + shield_amount, max_shield)
        elif item.effect == "destroy_enemies":
            self.enemies.clear()  # Hủy tất cả kẻ địch trên màn hình

    def game_loop(self, screen):
        clock = pygame.time.Clock()
        screen_width = screen.get_width()
        screen_height = screen.get_height()

        player = Player(screen_width, screen_height)
        score = 0
        running = True

        while running:
            screen.blit(self.background_image, (0, 0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
                    player.can_shoot = True

            keys = pygame.key.get_pressed()
            player.move(keys)
            if keys[pygame.K_SPACE]:
                player.shoot()

            player.update_bullets()

            current_time = pygame.time.get_ticks()

            # Logic sinh kẻ địch
            if current_time - self.last_spawn_time > self.spawn_delay:
                self.enemies.append(Enemy())
                self.last_spawn_time = current_time

            # Logic rơi vật phẩm
            if current_time - self.last_item_drop_time > self.item_drop_interval:
                new_item = DropItem(screen_width, screen_height)
                self.items.append(new_item)
                self.last_item_drop_time = current_time

            # Cập nhật và vẽ các kẻ địch
            for enemy in self.enemies:
                enemy.move()
                enemy.draw(screen)
                if random.randint(0, 150) == 0:
                    enemy.shoot()
                enemy.update_bullets()

            # Kiểm tra va chạm giữa người chơi và vật phẩm
            for item in self.items[:]:
                if player.rect.colliderect(item.rect):
                    self.apply_item_effect(player, item)
                    self.items.remove(item)

            # Xử lý va chạm giữa đạn của người chơi và kẻ địch
            for bullet in player.bullets[:]:
                for enemy in self.enemies[:]:
                    if bullet.colliderect(enemy.rect):
                        player.bullets.remove(bullet)
                        self.enemies.remove(enemy)
                        score += 1
                        break

            # Xử lý va chạm giữa đạn của kẻ địch và người chơi
            for enemy in self.enemies:
                for bullet in enemy.bullets[:]:
                    if bullet.colliderect(player.rect):
                        enemy.bullets.remove(bullet)
                        if player.lose_health():
                            running = False

            # Xử lý va chạm giữa người chơi và kẻ địch
            for enemy in self.enemies[:]:
                if enemy.rect.colliderect(player.rect):
                    self.enemies.remove(enemy)
                    if player.lose_health():
                        running = False

            # Vẽ người chơi, vật phẩm và các yếu tố giao diện
            player.draw(screen)
            for item in self.items:
                item.move()
                item.draw(screen)
            self.draw_text(f"Score: {score}", 10, 10, screen)
            self.draw_text(f"Lives: {player.lives}", 10, 80, screen)

            pygame.display.flip()
            clock.tick(60)

        return score
