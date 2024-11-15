import pygame
from player import Player
from enemy import Enemy
from high_score_manager import HighScoreManager
from constants import *
import random
from enemy_formation import *
from drop_item import DropItem  # Import DropItem


class Game:
    def __init__(self):
        self.high_score_manager = HighScoreManager("high_score.txt")
        self.background_image = pygame.image.load(
            "Images/background.png"
        ).convert()  # Load your background image
        self.item_drop_interval = config["item_drop_interval"]  # Set item drop interval
        self.last_item_drop_time = pygame.time.get_ticks()
        self.items = []  # Initialize list for items

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
            enemies.clear()  # Clear all enemies if item effect is destroy_enemies

    def start_menu(self, screen):
        menu_running = True
        while menu_running:
            screen.blit(self.background_image, (0, 0))  # Draw background
            pygame.draw.rect(
                screen, (255, 255, 255), (150, 100, 500, 400), border_radius=10
            )  # Menu background

            self.draw_text("Space Shooter", screen_width // 2 - 100, 130, screen)

            buttons = [
                ("Play", (200, 200)),
                ("High Score", (200, 250)),
                ("Reset High Score", (200, 300)),
                ("Exit", (200, 350)),
            ]

            for text, (x, y) in buttons:
                button_rect = pygame.Rect(x, y, 400, 40)
                pygame.draw.rect(
                    screen, (0, 120, 215), button_rect, border_radius=5
                )  # Button background
                self.draw_text(text, x + 150, y + 5, screen, white)

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        return "play"
                    if event.key == pygame.K_2:
                        return "high_score"
                    if event.key == pygame.K_3:
                        self.high_score_manager.reset_high_score()
                    if event.key == pygame.K_4:
                        pygame.quit()
                        quit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos
                    for i, (_, (x, y)) in enumerate(buttons):
                        button_rect = pygame.Rect(x, y, 400, 40)
                        if button_rect.collidepoint(mouse_pos):
                            if i == 0:  # Play
                                return "play"
                            elif i == 1:  # High Score
                                return "high_score"
                            elif i == 2:  # Reset High Score
                                self.high_score_manager.reset_high_score()
                            elif i == 3:  # Exit
                                pygame.quit()
                                quit()

    def game_loop(self, screen):
        player = Player(screen_width, screen_height)
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

            # Move and display enemies
            for enemy in enemies:
                enemy.move()
                enemy.draw(screen)
                if random.randint(0, 400) == 0:
                    enemy.shoot()
                enemy.update_bullets()

            # Check for bullet-enemy collision
            for bullet in player.bullets:
                for enemy in enemies:
                    if bullet.colliderect(enemy.rect):
                        player.bullets.remove(bullet)
                        enemies.remove(enemy)
                        score += 1
                        break

            # Check for bullet-enemy bullet collision
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

            # Check for player-enemy collision
            for enemy in enemies:
                if enemy.rect.colliderect(
                    pygame.Rect(player.x, player.y, spaceship_width, spaceship_height)
                ):
                    enemies.remove(enemy)
                    if player.lose_health():
                        running = False

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

        return score

    def game_over_menu(self, score, screen):
        high_score = self.high_score_manager.high_score
        if score > high_score:
            high_score = score
            self.high_score_manager.save_high_score(score)

        game_over_running = True
        while game_over_running:
            screen.blit(self.background_image, (0, 0))  # Draw background
            self.draw_text("Game Over!", screen_width // 2 - 100, 100, screen)
            self.draw_text(f"Your Score: {score}", screen_width // 2 - 100, 200, screen)
            self.draw_text(
                f"High Score: {high_score}", screen_width // 2 - 100, 250, screen
            )
            self.draw_text("1. Retry", screen_width // 2 - 50, 300, screen)
            self.draw_text("2. Quit", screen_width // 2 - 50, 350, screen)
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        return "retry"
                    if event.key == pygame.K_2:
                        pygame.quit()
                        quit()

    def show_high_score(self, screen):
        high_score_running = True
        while high_score_running:
            screen.blit(self.background_image, (0, 0))  # Draw background
            self.draw_text(
                f"High Score: {self.high_score_manager.high_score}",
                screen_width // 2 - 100,
                200,
                screen,
            )
            self.draw_text(
                "Press any key to return to the menu",
                screen_width // 2 - 150,
                300,
                screen,
            )
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    return

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
