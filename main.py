import pygame
from game import Game
from high_score_manager import HighScoreManager
from constants import *


def draw_text(text, x, y, screen, color=white, font_size=35):
    font = pygame.font.SysFont("Arial", font_size)
    screen_text = font.render(text, True, color)
    screen.blit(screen_text, (x, y))

def spaceship_selection_menu(screen, config):
    spaceships = config["spaceships"]
    selected_index = 0  # Chỉ số của máy bay được chọn

    while True:
        screen.fill(black)

        # Hiển thị tiêu đề
        draw_text("CHOOSE YOUR SPACESHIP", screen.get_width() // 2 - 200, 50, screen)

        # Hiển thị thông tin từng máy bay
        for i, spaceship in enumerate(spaceships):
            color = green if i == selected_index else white
            draw_text(
                f"{spaceship['name']} (HP: {spaceship['hp']}, Damage: {spaceship['damage']}, Speed: {spaceship['speed']})",
                100,
                150 + i * 100,
                screen,
                color,
            )
            spaceship_image = pygame.image.load(spaceship["image"]).convert_alpha()
            screen.blit(spaceship_image, (600, 150 + i * 100))

        draw_text("Press ENTER to select", 100, 500, screen)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    selected_index = (selected_index - 1) % len(spaceships)
                elif event.key == pygame.K_DOWN:
                    selected_index = (selected_index + 1) % len(spaceships)
                elif event.key == pygame.K_RETURN:
                    return spaceships[selected_index]

def main_menu(screen, high_score_manager):
    # Load the menu background image
    menu_background = pygame.image.load("Images/menu_background.png").convert()
    menu_background = pygame.transform.scale(
        menu_background, (screen_width, screen_height)
    )

    while True:
        screen.blit(menu_background, (0, 0))  # Draw the background image

        # Draw menu text on top of the background
        draw_text("MAIN MENU", screen.get_width() // 2 - 100, 100, screen)
        draw_text("1. Play", screen.get_width() // 2 - 100, 200, screen)
        draw_text("2. Show High Score", screen.get_width() // 2 - 100, 300, screen)
        draw_text("3. Reset High Score", screen.get_width() // 2 - 100, 400, screen)
        draw_text("4. Exit", screen.get_width() // 2 - 100, 500, screen)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "exit"
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_1:
                    return "play"
                elif event.key == pygame.K_2:
                    return "show_high_score"
                elif event.key == pygame.K_3:
                    high_score_manager.reset_high_score()
                elif event.key == pygame.K_4:
                    return "exit"


def show_high_score(screen, high_score_manager):
    screen.fill(black)
    draw_text("HIGH SCORE", screen.get_width() // 2 - 100, 100, screen)
    draw_text(
        f"High Score: {high_score_manager.high_score}",
        screen.get_width() // 2 - 100,
        200,
        screen,
    )
    draw_text(
        "Press M to return to Main Menu", screen.get_width() // 2 - 200, 300, screen
    )
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "exit"
            elif event.type == pygame.KEYUP and event.key == pygame.K_m:
                return "main_menu"


if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Space Shooter Game")

    high_score_manager = HighScoreManager("high_score.txt")
    game = Game()

    while True:
        action = main_menu(screen, high_score_manager)

        if action == "play":
            spaceship_data = spaceship_selection_menu(screen, config)
            if spaceship_data is None:
                break  # Thoát nếu người dùng đóng game
            result = game.game_loop(screen, spaceship_data)  # Truyền thông tin máy bay vào game loop
            if result == "exit":
                break
        elif action == "show_high_score":
            result = show_high_score(screen, high_score_manager)
            if result == "exit":
                break
        elif action == "exit":
            break

    pygame.quit()