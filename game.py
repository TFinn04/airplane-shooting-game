import pygame
from player import Player
from enemy import Enemy
from high_score_manager import HighScoreManager
from constants import *
import random
from enemy_formation import *
from drop_item import DropItem  # Import DropItem
import time

class Meteor:
    def __init__(self, screen_width, screen_height):
        self.image = pygame.image.load("Images/meteor.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, max(0, screen_width - self.rect.width))
        self.rect.y = -self.rect.height
        self.speed_y = random.randint(5, 10)  # Tốc độ rơi dọc (Y)
        self.speed_x = random.choice([-1, 1]) * random.randint(3, 7)  # Tốc độ ngang (X)

    def move(self):
        self.rect.y += self.speed_y  # Di chuyển theo trục Y
        self.rect.x += self.speed_x  # Di chuyển theo trục X

        # Đảo chiều nếu thiên thạch chạm rìa màn hình
        if self.rect.x <= 0 or self.rect.x >= screen_width - self.rect.width:
            self.speed_x = -self.speed_x  # Đảo chiều ngang

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def off_screen(self, screen_height):
        return self.rect.y > screen_height
    
    
class Game:
    def __init__(self):
        self.high_score_manager = HighScoreManager("high_score.txt")
        self.background_image = pygame.image.load(
            "Images/background.png"
        ).convert()  # Tải hình nền
        self.item_drop_interval = config["item_drop_interval"]  # Đặt khoảng thời gian thả vật phẩm
        self.last_item_drop_time = pygame.time.get_ticks()
        self.items = []  # Khởi tạo danh sách vật phẩm
        self.meteors = []  # Danh sách thiên thạch
        self.meteor_spawn_interval = 3  # Khoảng thời gian tạo thiên thạch (giây)
        self.last_meteor_spawn_time = time.time()

    def draw_text(self, text, x, y, screen, color=white):
        font = pygame.font.SysFont("Arial", 35)
        screen_text = font.render(text, True, color)
        screen.blit(screen_text, [x, y])

    def apply_item_effect(self, player, item, enemies):
        """Áp dụng hiệu ứng của vật phẩm cho người chơi"""
        if item.effect == "regen":
            player.health = min(player.health + regen_amount, max_health)
        elif item.effect == "shield":
            player.shield = min(player.shield + shield_amount, max_shield)
        elif item.effect == "destroy_enemies":
            enemies.clear()  # Xóa tất cả kẻ thù nếu hiệu ứng của vật phẩm là phá hủy kẻ thù

    def spawn_meteor(self):
        """Sinh thiên thạch sau khoảng thời gian định sẵn"""
        if time.time() - self.last_meteor_spawn_time > self.meteor_spawn_interval:
            self.meteors.append(Meteor(screen_width, screen_height))
            self.last_meteor_spawn_time = time.time()

    def update_meteors(self, screen):
        """Cập nhật vị trí và trạng thái của thiên thạch"""
        for meteor in self.meteors:
            meteor.move()
            meteor.draw(screen)

        # Xóa thiên thạch ra khỏi màn hình
        self.meteors = [meteor for meteor in self.meteors if not meteor.off_screen(screen_height)]

    def check_meteor_collisions(self, player, enemies):
        """Kiểm tra va chạm của thiên thạch"""
        for meteor in self.meteors:
            # Va chạm giữa thiên thạch và người chơi
            if player.rect.colliderect(meteor.rect):
                player.health -= 20  # Trừ máu người chơi

            # Va chạm giữa thiên thạch và kẻ địch
            for enemy in enemies[:]:
                if meteor.rect.colliderect(enemy.rect):
                    enemies.remove(enemy)  # Loại bỏ kẻ địch

    def game_loop(self, screen):
        player = Player(screen_width, screen_height)
        enemies = []
        score = 0
        running = True

        clock = pygame.time.Clock()

        while running:
            screen.blit(self.background_image, (0, 0))  # Vẽ hình nền

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_SPACE:
                        player.can_shoot = True

            keys = pygame.key.get_pressed()
            player.move(keys)

            if keys[pygame.K_SPACE]:
                player.shoot()

            player.update_bullets()

            # Sinh kẻ thù định kỳ
            if random.randint(0, 50) == 0:
                enemies.append(
                    Enemy(
                        random.randint(0, screen_width - enemy_width), -enemy_height, 0
                    )
                )

            # Sinh kẻ thù theo đội hình
            if random.randint(0, 300) == 0:
                enemies = enemies + new_formation()

            # Thả vật phẩm định kỳ
            current_time = pygame.time.get_ticks()
            if current_time - self.last_item_drop_time > self.item_drop_interval:
                new_item = DropItem(screen_width, screen_height)
                self.items.append(new_item)
                self.last_item_drop_time = current_time

            # Di chuyển và hiển thị kẻ thù
            for enemy in enemies:
                enemy.move()
                enemy.draw(screen)
                if random.randint(0, 400) == 0:
                    enemy.shoot()
                enemy.update_bullets()

            # Kiểm tra va chạm giữa đạn và kẻ thù
            for bullet in player.bullets:
                for enemy in enemies:
                    if bullet.colliderect(enemy.rect):
                        player.bullets.remove(bullet)
                        enemies.remove(enemy)
                        score += 1
                        break

            # Kiểm tra va chạm giữa người chơi và kẻ thù
            for enemy in enemies[:]:
                if enemy.rect.colliderect(
                    pygame.Rect(player.x, player.y, spaceship_width, spaceship_height)
                ):
                    enemies.remove(enemy)
                    if player.lose_health():
                        running = False

            # Kiểm tra va chạm giữa người chơi và vật phẩm
            for item in self.items[:]:
                if player.rect.colliderect(item.rect):
                    self.apply_item_effect(player, item, enemies)
                    self.items.remove(item)

            # Cập nhật và xử lý thiên thạch
            self.spawn_meteor()
            self.update_meteors(screen)
            self.check_meteor_collisions(player, enemies)
            pygame.display.flip()

            # Loại bỏ kẻ thù ra khỏi màn hình
            enemies = [enemy for enemy in enemies if enemy.rect.y < screen_height]

            # Vẽ người chơi, vật phẩm và điểm số
            player.draw(screen)
            for item in self.items:
                item.move()
                item.draw(screen)

            self.draw_text(f"Score: {score}", 10, 10, screen)
            self.draw_text(f"Lives: {player.lives}", 10, 80, screen)

            pygame.display.flip()
            clock.tick(60)

        self.display_score(screen, score)
        return score

    def display_score(self, screen, score):
        """Hiển thị điểm sau khi kết thúc trò chơi"""
        screen.fill(black)
        self.draw_text(f"Game Over", screen.get_width() // 2 - 100, 100, screen)
        self.draw_text(f"Score: {score}", screen.get_width() // 2 - 100, 200, screen)
        self.draw_text(
            "Press M to return to Main Menu", screen.get_width() // 2 - 200, 300, screen
        )
        pygame.display.flip()

        # Chờ người chơi nhấn phím để quay lại menu chính
        waiting_for_input = True
        while waiting_for_input:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_m:
                        waiting_for_input = False  # Thoát vòng lặp và quay lại menu chính
                    elif event.key == pygame.K_q:
                        pygame.quit()  # Thoát trò chơi nếu nhấn 'Q'
                        quit()

    def run(self, screen):
        while True:
            choice = self.start_menu(screen)

            if choice == "play":
                score = self.game_loop(screen)
                game_over_choice = self.game_over_menu(score, screen)
                if game_over_choice == "retry":
                    continue

            elif choice == "high_score":
                self.show_high_score(screen)
