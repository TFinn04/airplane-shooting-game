import pygame
from player import Player
from enemy import Enemy
from high_score_manager import HighScoreManager
from constants import *
from background_elements import *
import random
from enemy_formation import *
from drop_item import DropItem  # Import DropItem
from boss import Boss
import time
from meteor import Meteor


class Game:
    def __init__(self):

        pygame.mixer.init()
        # Hiệu ứng âm thanh
        self.shoot_sound = pygame.mixer.Sound("Sounds/shoot.wav")
        self.enemy_hit_sound = pygame.mixer.Sound("Sounds/hit.wav")
        self.item_pickup_sound = pygame.mixer.Sound("Sounds/item_pickup.wav")
        self.meteor_sound = pygame.mixer.Sound("Sounds/meteor.wav")
        self.shoot_sound.set_volume(0.25)
        self.enemy_hit_sound.set_volume(0.25)
        self.item_pickup_sound.set_volume(0.25)
        self.meteor_sound.set_volume(0.25)

        self.high_score_manager = HighScoreManager("high_score.txt")
        # Preload all background images
        self.background_images = [
            pygame.image.load(f"Images/background/background{i}.png").convert()
            for i in range(1, 10)
        ]
        self.current_background_index = 0
        self.last_background_switch_time = pygame.time.get_ticks()

        self.game_over_images = [
            pygame.image.load(f"Images/gameover/gameover{i}.png").convert()
            for i in range(
                1, 12
            )  # Assuming images are named gameover1.png to gameover10.png
        ]
        self.current_game_over_index = 0
        self.current_background_index = 0
        self.last_game_over_switch_time = pygame.time.get_ticks()

        self.item_drop_interval = config["item_drop_interval"]  # Set item drop interval
        self.last_item_drop_time = pygame.time.get_ticks()
        self.items = []  # Khởi tạo danh sách vật phẩm
        self.meteors = []  # Danh sách thiên thạch
        self.meteor_spawn_interval = 3.5  # Khoảng thời gian tạo thiên thạch (giây)
        self.last_meteor_spawn_time = time.time()
        self.last_planet_spawn_time = time.time()
        self.boss_active = False  # Flag to track if boss spawn is active
        self.last_boss = 0  # Track last score milestone for boss appearance
        self.boss = None
        self.boss_spawntime = 0
        self.boss_deathtime = 0
        self.boss_act = False
        self.boss_action = 0
        self.cheat = True

        # Preload images
        self.heart_icon = pygame.image.load("Images/lives.png").convert_alpha()
        self.heart_icon = pygame.transform.scale(
            self.heart_icon, (30, 30)
        )  # Resize as needed

        self.score_board = pygame.image.load("Images/score_board.png").convert_alpha()
        self.score_board = pygame.transform.scale(
            self.score_board, (100, 30)
        )  # Resize as needed

    def draw_text(
        self,
        text,
        x,
        y,
        screen,
        font_path="Fonts/orbitron.ttf",
        font_size=30,
        color=white,
    ):
        """Draw text with a custom font and style."""
        try:
            font = pygame.font.Font(font_path, font_size)
        except FileNotFoundError:
            font = pygame.font.SysFont("Arial", font_size)

        text_surface = font.render(text, True, color)
        screen.blit(text_surface, (x, y))

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
        self.meteors = [
            meteor for meteor in self.meteors if not meteor.off_screen(screen_height)
        ]

    def check_meteor_collisions(self, player, enemies):
        """Kiểm tra va chạm của thiên thạch"""
        for meteor in self.meteors:
            # Va chạm giữa thiên thạch và người chơi
            if player.rect.colliderect(meteor.rect):
                player.health -= 5  # Trừ máu người chơi

                # Nếu máu người chơi <= 0, trừ mạng và reset máu
                if player.health <= 0:
                    player.lives -= 1  # Trừ một mạng
                    player.health = (
                        100  # Reset máu về 100 (hoặc giá trị tối đa của bạn)
                    )

                    # Kiểm tra nếu người chơi hết mạng
                    if player.lives <= 0:
                        return True

            # Va chạm giữa thiên thạch và kẻ địch
            for enemy in enemies[:]:
                if meteor.rect.colliderect(enemy.rect):
                    enemies.remove(enemy)  # Loại bỏ kẻ địch
                    self.meteor_sound.play()

    # Add bullet at (x,y)

    def enemy_shoot(self, X, Y, screen):
        bullet = pygame.Rect(
            X + enemy_width // 2 - bullet_width // 2,
            Y + enemy_height,
            bullet_width,
            bullet_height // 3,
        )

        return bullet

    def game_loop(self, screen, spaceship_data):
        player = Player(spaceship_data, screen_width, screen_height)
        enemies = []
        bullets = []
        score = 0
        running = True
        cheat = True
        bullet_image = pygame.image.load("Images/enemy_bullet.png")

        clock = pygame.time.Clock()

        while running:
            # Update background dynamically
            current_time = pygame.time.get_ticks()
            if current_time - self.last_background_switch_time > 100:
                self.current_background_index = (
                    self.current_background_index + 1
                ) % len(self.background_images)
                self.last_background_switch_time = current_time

            # Draw the current background
            screen.blit(self.background_images[self.current_background_index], (0, 0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_SPACE:
                        player.can_shoot = True
                    if pygame.K_0 <= event.key <= pygame.K_5:
                        cheat = True

            keys = pygame.key.get_pressed()

            player.move(keys)

            if keys[pygame.K_SPACE]:
                player.shoot()
                self.shoot_sound.play()

            if cheat:
                if keys[pygame.K_0]:
                    enemies.append(Enemy(screen_width // 2, -enemy_height, 0))
                    cheat = False
                if keys[pygame.K_1]:
                    enemies = enemies + formation1(score)
                    cheat = False
                if keys[pygame.K_2]:
                    enemies = enemies + formation2(score)
                    cheat = False
                if keys[pygame.K_3]:
                    enemies = enemies + formation3(score)
                    cheat = False
                if keys[pygame.K_4]:
                    enemies = enemies + formation4(score)
                    cheat = False
                if keys[pygame.K_5]:
                    self.boss = Boss()
                    self.boss_active = True
                    self.last_boss = score  # Update last boss score
                    self.boss_spawntime = time.time()
                    self.boss_action = time.time()
                    cheat = False

            player.update_bullets()
            # spawn planets as background element
            # if time.time() - self.last_planet_spawn_time > 10:
            #   planets.append(Planets(screen_width, screen_height))
            #    self.last_planet_spawn_time = time.time()
            # for planet in planets:
            #    planet.move()
            #    planet.draw(screen)
            # planets = [planet for planet in planets if not planet.off_screen(screen_height)]
            # spawn boss when reach required score

            # spawn boss when reach required score
            if (
                score % 50 == 0
                and score > 0
                and score != self.last_boss
                and not self.boss_active
            ):
                self.boss = Boss()
                self.boss_active = True
                self.last_boss = score  # Update last boss score
                self.boss_spawntime = time.time()
                self.boss_action = time.time()

            # Spawn things if boss not active
            if not self.boss_active:
                # Spawn enemies at intervals
                if random.randint(0, max(abs(100 - score), 50)) == 0:
                    enemies.append(
                        Enemy(
                            random.randint(0, screen_width - enemy_width),
                            -enemy_height,
                            0,
                        )
                    )

                # Spawn enemies in formations
                if random.randint(0, max(abs(500 - score), 500)) == 0:
                    enemies = enemies + new_formation(score)

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
                if self.check_meteor_collisions(player, enemies):
                    self.display_score(screen, score)  # Hiển thị màn hình Game Over
                    running = False
                    continue  # Thoát khỏi vòng lặp game

            # Delay for boss spawn and death
            if self.boss_active:
                if (
                    time.time() - self.boss_spawntime < 5
                    and time.time() - self.boss_spawntime >= 2
                    and self.boss_spawntime != 0
                ):
                    elapsed_time = time.time() - self.boss_spawntime
                    frame_index = int(elapsed_time * 20) % 20

                    # Load the corresponding image
                    warning_image_path = f"Images/warning/warning{frame_index + 1}.png"
                    warning_image = pygame.image.load(
                        warning_image_path
                    ).convert_alpha()

                    # Center the image on the screen
                    warning_rect = warning_image.get_rect(
                        center=(screen_width // 2, screen_height // 2)
                    )
                    screen.blit(warning_image, warning_rect)

                if time.time() - self.boss_spawntime >= 5 and self.boss_spawntime != 0:
                    self.boss.move()  # Move boss downward to the target position
                    self.boss.draw(screen)  # Draw the boss

                elif (
                    time.time() - self.boss_deathtime >= 4 and self.boss_deathtime != 0
                ):
                    self.boss_deathtime = 0
                    self.boss_active = False

            # Boss actions
            if self.boss:
                if not self.boss_act and time.time() - self.boss_action >= 10:
                    self.boss_action = random.choice(
                        [time.time() - 10, time.time() - 27]
                    )
                    self.boss_act = True
                if (time.time() - self.boss_action) >= 10 and (
                    time.time() - self.boss_action
                ) < 25:
                    self.boss.attack1()
                self.boss.update_bullets()
                if (time.time() - self.boss_action) >= 25 and (
                    time.time() - self.boss_action
                ) <= 26:
                    self.boss_act = False
                    self.boss_action = time.time() - 7
                if (time.time() - self.boss_action) > 26 and (
                    time.time() - self.boss_action
                ) < 35:
                    if not self.boss.charging and not self.boss.beam_active:
                        target_x = player.rect.centerx - boss_width / 2
                    if self.boss.rect.x < target_x - 5:
                        self.boss.rect.x += boss_speed * 7
                    if self.boss.rect.x > target_x + 5:
                        self.boss.rect.x -= boss_speed * 7
                    self.boss.attack2()
                if (time.time() - self.boss_action) >= 36 and (
                    time.time() - self.boss_action
                ) <= 37:
                    self.boss_act = False
                    self.boss_action = time.time() - 7
                self.boss.update_attack2()
                if self.boss.beam_active:
                    # Check for beam collision with player
                    beam_rect = pygame.Rect(
                        self.boss.rect.centerx - beam_width // 2,
                        self.boss.rect.bottom,
                        beam_width,
                        beam_height,
                    )
                    if beam_rect.colliderect(
                        pygame.Rect(
                            player.x, player.y, spaceship_width, spaceship_height
                        )
                    ):
                        if player.lose_health_dot():
                            running = False
                            self.boss_active = False
                            self.boss = None

            # Move and display enemies
            for enemy in enemies:
                enemy.move()
                enemy.draw(screen)
                if random.randint(0, max(abs(250 - score), 150)) == 0:
                    bullets.append(self.enemy_shoot(enemy.rect.x, enemy.rect.y, screen))
            for bullet in bullets:
                bullet.y += enemy_bullet_speed
                screen.blit(bullet_image, (bullet.x, bullet.y))

            bullets = [bullet for bullet in bullets if bullet.y < screen_height]

            # Check for bullet-enemy and bullet-boss collision
            for bullet in player.bullets:
                if self.boss:
                    if bullet.colliderect(self.boss.rect):
                        player.bullets.remove(bullet)
                        self.boss.health -= (
                            player.damage
                        )  # Reduce boss health by player's damage
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
                        self.enemy_hit_sound.play()
                        break

            # Check for player-boss collision
            if self.boss and self.boss.rect.colliderect(
                pygame.Rect(player.x, player.y, player.width, player.height)
            ):
                if player.lose_health_dot():
                    running = False
                    self.boss_active = False
                    self.boss = None

            # Check for player-enemy bullet collision
            
            for bullet in bullets:
                if bullet.colliderect(
                    pygame.Rect(
                        player.x, player.y, spaceship_width, spaceship_height
                    )
                ):
                    bullets.remove(bullet)
                    if player.lose_health():
                        running = False
                        if self.boss_active:
                            self.boss_active = False
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
                            self.boss_active = False
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
                            self.boss_active = False
                            self.boss = None

            # Check for player-item collision
            for item in self.items[:]:
                if player.rect.colliderect(item.rect):
                    self.apply_item_effect(player, item, enemies)
                    self.items.remove(item)
                    self.item_pickup_sound.play()

            # Remove enemies that are off-screen
            enemies = [enemy for enemy in enemies if enemy.rect.y < screen_height]

            # Draw player, items, and score
            player.draw(screen)
            for item in self.items:
                item.move()
                item.draw(screen)

            # Draw the score board background
            screen.blit(self.score_board, (10, 10))

            # Draw the score text
            self.draw_text(
                "Score: " f"{score}", 30, 15, screen, font_size=18, color=(0, 0, 0)
            )

            # Draw the lives icons
            for i in range(player.lives):
                screen.blit(self.heart_icon, (10 + i * 45, 70))

            pygame.display.flip()
            clock.tick(60)

        self.display_score(screen, score)
        return score

    def display_score(self, screen, score):

        # Load custom font (use a TTF file for sci-fi style fonts)
        try:
            font_path = "Fonts/orbitron.ttf"  # Replace with your sci-fi font path
            title_font = pygame.font.Font(font_path, 80)
            text_font = pygame.font.Font(font_path, 40)
        except FileNotFoundError:
            # Fallback to default font if custom font is not found
            title_font = pygame.font.SysFont("Arial", 70, bold=True)
            text_font = pygame.font.SysFont("Arial", 20, bold=True)
            text1_font = pygame.font.SysFont("Arial", 30, bold=True)

        # Initialize variables for animation
        alpha = 0  # Fade effect for "Game Over"
        blink_timer = pygame.time.get_ticks()
        blink_interval = 500
        blink = True
        zoom_factor = 1.0
        zoom_direction = 1

        # Loop for the Game Over screen
        waiting_for_input = True
        while waiting_for_input:
            # Draw the background image
            current_time = pygame.time.get_ticks()
            if current_time - self.last_game_over_switch_time > 100:
                self.current_game_over_index = (self.current_game_over_index + 1) % len(
                    self.game_over_images
                )
                self.last_game_over_switch_time = current_time

            screen.blit(self.game_over_images[self.current_game_over_index], (0, 0))

            # Apply zoom effect to "Game Over"
            if zoom_direction == 1:
                zoom_factor += 0.002
                if zoom_factor >= 1.2:
                    zoom_direction = -1
            else:
                zoom_factor -= 0.002
                if zoom_factor <= 1.0:
                    zoom_direction = 1

            # Render "Game Over" with fade and zoom effects
            title_surface = title_font.render("Game Over", True, (176, 196, 222))
            title_surface = pygame.transform.scale(
                title_surface,
                (
                    int(title_surface.get_width() * zoom_factor),
                    int(title_surface.get_height() * zoom_factor),
                ),
            )
            title_rect = title_surface.get_rect(center=(screen.get_width() // 2, 150))
            screen.blit(title_surface, title_rect)

            # Render score and instructions
            score_surface = text1_font.render(f"Score: {score}", True, (176, 196, 222))
            score_rect = score_surface.get_rect(center=(screen.get_width() // 2, 250))
            screen.blit(score_surface, score_rect)

            if blink:
                menu_surface = text_font.render(
                    "Press M to return to Main Menu", True, (176, 196, 222)
                )
                menu_rect = menu_surface.get_rect(center=(screen.get_width() // 2, 350))
                screen.blit(menu_surface, menu_rect)

                quit_surface = text_font.render(
                    "Press Q to Quit", True, (176, 196, 222)
                )
                quit_rect = quit_surface.get_rect(center=(screen.get_width() // 2, 400))
                screen.blit(quit_surface, quit_rect)

            # Handle blinking effect
            current_time = pygame.time.get_ticks()
            if current_time - blink_timer > blink_interval:
                blink = not blink
                blink_timer = current_time

            # Update the display
            pygame.display.flip()

            # Handle user input
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
