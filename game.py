import pygame
import random
from drop_item import DropItem
from player import Player
from enemy import Enemy
from high_score_manager import HighScoreManager
from constants import *  # Import constants


class Game:
    def __init__(self):
        self.high_score_manager = HighScoreManager("high_score.txt")
        self.background_image = pygame.image.load("Images/background.png").convert()
        self.last_spawn_time = pygame.time.get_ticks()
        self.spawn_delay = config["enemy_spawn_delay"]
        self.item_drop_interval = config["item_drop_interval"]
        self.last_item_drop_time = pygame.time.get_ticks()
        self.items = []
        self.enemies = []

    def draw_text(self, text, x, y, screen, color=white):
        font = pygame.font.SysFont("Arial", 35)
        screen_text = font.render(text, True, color)
        screen.blit(screen_text, (x, y))

    def apply_item_effect(self, player, item):
        if item.effect == "regen":
            player.health = min(player.health + regen_amount, max_health)
        elif item.effect == "shield":
            player.shield = min(player.shield + shield_amount, max_shield)
        elif item.effect == "destroy_enemies":
            self.enemies.clear()

    def game_loop(self, screen):
        clock = pygame.time.Clock()
        screen_width = screen.get_width()
        screen_height = screen.get_height()

        # Initialize/reset player, enemies, items, and score for each new game
        player = Player(screen_width, screen_height)
        self.enemies = []  # Clear previous enemies
        self.items = []  # Clear previous items
        score = 0
        running = True

        while running:
            screen.blit(self.background_image, (0, 0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_SPACE:
                        player.can_shoot = True
                    elif event.key == pygame.K_m and player.lives <= 0:
                        return "main_menu"

            keys = pygame.key.get_pressed()
            player.move(keys)
            if keys[pygame.K_SPACE]:
                player.shoot()

            player.update_bullets()

            # Spawn enemies and items at intervals
            current_time = pygame.time.get_ticks()
            if current_time - self.last_spawn_time > self.spawn_delay:
                # Provide random x, y positions and a random status for the enemy
                enemy_x = random.randint(0, screen_width - enemy_width)
                enemy_y = random.randint(-100, -enemy_height)  # Start above the screen
                status = random.choice(
                    [0, 1, 2, 3, -1, -2, -3]
                )  # Random enemy formation status
                self.enemies.append(
                    Enemy(enemy_x, enemy_y, status)
                )  # Pass values to the Enemy constructor
                self.last_spawn_time = current_time
            if current_time - self.last_item_drop_time > self.item_drop_interval:
                new_item = DropItem(screen_width, screen_height)
                self.items.append(new_item)
                self.last_item_drop_time = current_time

            # Move and display enemies and bullets
            for enemy in self.enemies:
                enemy.move()
                enemy.draw(screen)
                if random.randint(0, 150) == 0:
                    enemy.shoot()
                enemy.update_bullets()

            # Check for player-item collision
            for item in self.items[:]:
                if player.rect.colliderect(item.rect):
                    self.apply_item_effect(player, item)
                    self.items.remove(item)

            # Handle bullet-enemy collision
            for bullet in player.bullets[:]:
                for enemy in self.enemies[:]:
                    if bullet.colliderect(enemy.rect):
                        player.bullets.remove(bullet)
                        self.enemies.remove(enemy)
                        score += 1
                        break

            # Handle enemy bullet-player collision
            for enemy in self.enemies:
                for bullet in enemy.bullets[:]:
                    if bullet.colliderect(player.rect):
                        enemy.bullets.remove(bullet)
                        if player.lose_health():
                            running = False

            # Handle player-enemy collision
            for enemy in self.enemies[:]:
                if enemy.rect.colliderect(player.rect):
                    self.enemies.remove(enemy)
                    if player.lose_health():
                        running = False

            # Draw player, items, and score
            player.draw(screen)
            for item in self.items:
                item.move()
                item.draw(screen)
            self.draw_text(f"Score: {score}", 10, 10, screen)
            self.draw_text(f"Lives: {player.lives}", 10, 80, screen)

            pygame.display.flip()
            clock.tick(60)

        if player.lives <= 0:
            # Display final score and high score after game over
            self.high_score_manager.save_high_score(
                max(score, self.high_score_manager.high_score)
            )
            while True:
                screen.blit(self.background_image, (0, 0))
                self.draw_text(
                    f"Final Score: {score}",
                    screen_width // 2 - 100,
                    screen_height // 2 - 50,
                    screen,
                )
                self.draw_text(
                    f"High Score: {self.high_score_manager.high_score}",
                    screen_width // 2 - 100,
                    screen_height // 2,
                    screen,
                )
                self.draw_text(
                    "Press M to return to Main Menu",
                    screen_width // 2 - 150,
                    screen_height // 2 + 50,
                    screen,
                )

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        return "exit"
                    elif event.type == pygame.KEYUP and event.key == pygame.K_m:
                        return "main_menu"

                pygame.display.flip()
                clock.tick(60)
