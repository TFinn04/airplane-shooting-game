import pygame
from player import Player
from enemy import Enemy
from high_score_manager import HighScoreManager
from constants import *
import random
from enemy_formation import *
from drop_item import DropItem  # Import DropItem
from boss import Boss
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
        ).convert()  # Load your background image
        self.item_drop_interval = config["item_drop_interval"]  # Set item drop interval
        self.last_item_drop_time = pygame.time.get_ticks()
        self.items = []  # Khởi tạo danh sách vật phẩm
        self.meteors = []  # Danh sách thiên thạch
        self.meteor_spawn_interval = 3  # Khoảng thời gian tạo thiên thạch (giây)
        self.last_meteor_spawn_time = time.time()
        self.boss_active = False  # Flag to track if boss spawn is active
        self.last_boss = 0  # Track last score milestone for boss appearance
        self.boss = None
        self.boss_spawntime = 0
        self.boss_deathtime = 0
        self.boss_act = False
        self.boss_action = 0

    def draw_text(self, text, x, y, screen, color=white):
        font = pygame.font.SysFont("Arial", 35)
        screen_text = font.render(text, True, color)
        screen.blit(screen_text, [x, y])

    def apply_item_effect(self, player, item, enemies):
        """Apply the effect of the item to the player"""
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

    def game_loop(self, screen, spaceship_data):
        player = Player(spaceship_data, screen_width, screen_height)
        enemies = []
        score = 0   
        running = True

        clock = pygame.time.Clock()

        while running:
            screen.blit(self.background_image, (0, 0))  # Draw background

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

            #spawn boss when reach required score
            if score % 50 == 0 and score > 0 and score != self.last_boss and not self.boss_active:
                self.boss = Boss()
                self.boss_active = True
                self.last_boss = score  # Update last boss score
                self.boss_spawntime = time.time()
                self.boss_action =time.time()

            # Spawn things if boss not active
            if not self.boss_active:
                # Spawn enemies at intervals
                if random.randint(0, 50) == 0:
                    enemies.append(
                        Enemy(
                            random.randint(0, screen_width - enemy_width), -enemy_height, 0
                        )
                    )
            
                # Spawn enemies in formations
                if random.randint(0, 300) == 0:
                    enemies = enemies + new_formation()

                # Drop items at regular intervals
                current_time = pygame.time.get_ticks()
                if current_time - self.last_item_drop_time > self.item_drop_interval:
                    new_item = DropItem(screen_width, screen_height)
                    self.items.append(new_item)
                    self.last_item_drop_time = current_time
                
                # Cập nhật và xử lý thiên thạch
                self.spawn_meteor()
                self.update_meteors(screen)
                self.check_meteor_collisions(player, enemies)
            
            # Delay for boss spawn and death
            if self.boss_active:
                if time.time() - self.boss_spawntime <= 5 and time.time() - self.boss_spawntime >= 2 and self.boss_spawntime != 0:
                    elapsed_time = time.time() - self.boss_spawntime
                    frame_index = int(elapsed_time * 20) % 20 

                    # Load the corresponding image
                    warning_image_path = f"Images/warning/warning{frame_index + 1}.png"
                    warning_image = pygame.image.load(warning_image_path).convert_alpha()

                    # Center the image on the screen
                    warning_rect = warning_image.get_rect(center=(screen_width // 2, screen_height // 2))
                    screen.blit(warning_image, warning_rect)

                if time.time() - self.boss_spawntime >= 6 and self.boss_spawntime!=0:
                    self.boss.move()  # Move boss downward to the target position
                    self.boss.draw(screen)  # Draw the boss
                
                elif time.time() - self.boss_deathtime >= 4 and self.boss_deathtime!=0:
                    self.boss_deathtime =0
                    self.boss_active = False

            # Boss actions
            if self.boss:
                if not self.boss_act and time.time() - self.boss_action >= 10:
                    self.boss_action = random.choice([time.time() - 10,time.time() -27])
                    self.boss_act = True
                if (time.time()- self.boss_action) >=10 and (time.time()- self.boss_action) <=22:
                    self.boss.attack1()
                if (time.time()- self.boss_action) <25 and (time.time()- self.boss_action) >22:
                    self.boss.reposition()
                self.boss.update_bullets()
                if (time.time()- self.boss_action) >=25 and (time.time()- self.boss_action) <=26:
                    self.boss_act=False
                    self.boss_action = time.time()-8
                if(time.time() - self.boss_action) >26 and (time.time()- self.boss_action) < 35:
                    self.boss.attack2()
                if(time.time() - self.boss_action) >=36 and (time.time()- self.boss_action) <= 37:
                    self.boss_act=False
                    self.boss_action = time.time()-7
                self.boss.update_attack2()
                if self.boss.beam_active:
                # Check for beam collision with player
                    beam_rect = pygame.Rect(
                        self.boss.rect.centerx - beam_width // 2,
                        self.boss.rect.bottom,
                        beam_width,
                        beam_height
                    )
                    if beam_rect.colliderect(pygame.Rect(player.x, player.y, spaceship_width, spaceship_height)):
                        if player.lose_health():
                            running = False
                            self.boss_active=False
                            self.boss = None

            # Move and display enemies
            for enemy in enemies:
                enemy.move()
                enemy.draw(screen)
                if random.randint(0, 400) == 0:
                    enemy.shoot()
                enemy.update_bullets()

            # Check for bullet-enemy and bullet-boss collision
            for bullet in player.bullets:
                if self.boss:
                    if bullet.colliderect(self.boss.rect):
                        player.bullets.remove(bullet)
                        self.boss.health -= player.damage  # Reduce boss health by player's damage
                        if self.boss.health <= 0:
                            score += 5  # Add score on boss defeat
                            self.boss = None  # Remove the boss
                            self.boss_deathtime = time.time()
                            self.boss_spawntime = 0

                for enemy in enemies:
                    if bullet.colliderect(enemy.rect):
                        player.bullets.remove(bullet)
                        enemies.remove(enemy)
                        score += 1
                        break
            
            # Check for player-boss collision
            if self.boss and self.boss.rect.colliderect(
                pygame.Rect(player.x, player.y, player.width, player.height)
            ):
                if player.lose_health:
                    running=False
                    self.boss_active=False
                    self.boss = None

            # Check for player-enemy bullet collision
            for enemy in enemies:
                for bullet in enemy.bullets:
                    if bullet.colliderect(
                        pygame.Rect(
                            player.x, player.y, spaceship_width, spaceship_height
                        )
                    ):
                        enemy.bullets.remove(bullet)
                        if player.lose_health():
                            running = False
                            if self.boss_active:
                                self.boss_active=False
                                self.boss = None

            # Check for player-boss bullet collision
            if self.boss:
                for bullet in self.boss.bullets:
                    if bullet.colliderect(
                        pygame.Rect(
                            player.x, player.y, spaceship_width, spaceship_height
                        )
                    ):
                        self.boss.bullets.remove(bullet)
                        if player.lose_health():
                            running = False
                            self.boss_active=False
                            self.boss = None

            # Check for player-enemy collision
            for enemy in enemies:
                if enemy.rect.colliderect(
                    pygame.Rect(player.x, player.y, spaceship_width, spaceship_height)
                ):
                    enemies.remove(enemy)
                    if player.lose_health():
                        running = False
                        if self.boss_active:
                            self.boss_active=False
                            self.boss = None

            # Check for player-item collision
            for item in self.items[:]:
                if player.rect.colliderect(item.rect):
                    self.apply_item_effect(player, item, enemies)
                    self.items.remove(item)


            # Remove enemies that are off-screen
            enemies = [enemy for enemy in enemies if enemy.rect.y < screen_height]

            # Draw player, items, and score
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
        """Display the score after game over"""
        screen.fill(black)
        self.draw_text(f"Game Over", screen.get_width() // 2 - 100, 100, screen)
        self.draw_text(f"Score: {score}", screen.get_width() // 2 - 100, 200, screen)
        self.draw_text(
            "Press M to return to Main Menu", screen.get_width() // 2 - 200, 300, screen
        )
        pygame.display.flip()

        # Wait for user input to return to the main menu
        waiting_for_input = True
        while waiting_for_input:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_m:
                        waiting_for_input = False  # Exit loop and return to main menu
                    elif event.key == pygame.K_q:
                        pygame.quit()  # Quit the game if 'Q' is pressed
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
