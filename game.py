import pygame
from player import Player
from enemy import Enemy
from high_score_manager import HighScoreManager
from constants import *
import random


class Game:
    def __init__(self):
        self.high_score_manager = HighScoreManager("high_score.txt")
        self.background_image = pygame.image.load(
            "background.png"
        ).convert()  # Load your background image

    def draw_text(self, text, x, y, screen, color=white):
        font = pygame.font.SysFont("Arial", 35)
        screen_text = font.render(text, True, color)
        screen.blit(screen_text, [x, y])

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
        player = Player()
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

            if random.randint(0, 50) == 0:
                enemies.append(Enemy())

            for enemy in enemies:
                enemy.move()
                enemy.draw(screen)

            for bullet in player.bullets:
                for enemy in enemies:
                    if bullet.colliderect(enemy.rect):
                        player.bullets.remove(bullet)
                        enemies.remove(enemy)
                        score += 1
                        break

            for enemy in enemies:
                if enemy.rect.colliderect(
                    pygame.Rect(player.x, player.y, spaceship_width, spaceship_height)
                ):
                    enemies.remove(enemy)
                    if player.lose_health():
                        running = False

            enemies = [enemy for enemy in enemies if enemy.rect.y < screen_height]

            player.draw(screen)

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
                else:
                    break
            elif choice == "high_score":
                self.show_high_score(screen)


if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((screen_width, screen_height))
    game = Game()
    game.run(screen)
    pygame.quit()
