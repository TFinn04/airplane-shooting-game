import pygame
from player import Player
from enemy import Enemy
from high_score_manager import HighScoreManager
import random
from constants import *  # Constants are imported from the constants file


class Game:
    def __init__(self):
        self.high_score_manager = HighScoreManager("high_score.txt")
        self.background_image = pygame.image.load(
            "background.png"
        ).convert()  # Load background

        # Enemy spawn delay configuration from config.json
        self.last_spawn_time = pygame.time.get_ticks()  # Initialize last spawn time
        self.spawn_delay = config[
            "enemy_spawn_delay"
        ]  # Get the spawn delay from config

    def draw_text(self, text, x, y, screen, color=white):
        # Create font object and render text on the screen
        font = pygame.font.SysFont("Arial", 35)
        screen_text = font.render(text, True, color)
        screen.blit(screen_text, (x, y))

    def game_loop(self, screen):
        clock = pygame.time.Clock()  # Control the frame rate

        player = Player(
            screen.get_width(), screen.get_height()
        )  # Initialize player object with screen dimensions
        enemies = []
        score = 0
        running = True

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

            # Check if it's time to spawn a new enemy (based on spawn delay)
            current_time = pygame.time.get_ticks()
            if current_time - self.last_spawn_time > self.spawn_delay:
                enemies.append(Enemy())  # Spawn new enemy
                self.last_spawn_time = current_time  # Update the last spawn time

            for enemy in enemies:
                enemy.move()
                enemy.draw(screen)
                if random.randint(0, 150) == 0:  # Random chance for enemy to shoot
                    enemy.shoot()
                enemy.update_bullets()

            # Handle collisions between player bullets and enemies
            for bullet in player.bullets:
                for enemy in enemies:
                    if bullet.colliderect(enemy.rect):
                        player.bullets.remove(bullet)
                        enemies.remove(enemy)
                        score += 1
                        break

            # Handle collisions between enemy bullets and player
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

            # Handle collisions between player and enemy
            for enemy in enemies:
                if enemy.rect.colliderect(
                    pygame.Rect(player.x, player.y, spaceship_width, spaceship_height)
                ):
                    enemies.remove(enemy)
                    if player.lose_health():
                        running = False

            # Remove off-screen enemies
            enemies = [enemy for enemy in enemies if enemy.rect.y < screen.get_height()]

            player.draw(screen)

            self.draw_text(f"Score: {score}", 10, 10, screen)
            self.draw_text(f"Lives: {player.lives}", 10, 80, screen)

            pygame.display.flip()
            clock.tick(60)  # 60 FPS

        return score  # Return the score when the game is over
