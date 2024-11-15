import pygame
from game import Game
from high_score_manager import HighScoreManager
from constants import *


def draw_text(text, x, y, screen, color=white, font_size=35):
    font = pygame.font.SysFont("Arial", font_size)
    screen_text = font.render(text, True, color)
    screen.blit(screen_text, (x, y))

def draw_gradient(screen, color1, color2):
    height = screen.get_height()
    for i in range(height):
        color = (
            int(color1[0] + (color2[0] - color1[0]) * i / height),
            int(color1[1] + (color2[1] - color1[1]) * i / height),
            int(color1[2] + (color2[2] - color1[2]) * i / height),
        )
        pygame.draw.line(screen, color, (0, i), (screen.get_width(), i))

# Hàm vẽ menu chọn tàu vũ trụ
def spaceship_selection_menu(screen, config):
    spaceships = config["spaceships"]
    selected_index = 0  # Chỉ số của tàu vũ trụ được chọn
    border_color = neon_blue  # Màu viền sáng cho tàu vũ trụ đang được chọn

    # Thiết lập font chữ
    font_title = pygame.font.Font(None, 48)  # Giảm kích thước font tiêu đề
    font_info = pygame.font.Font(None, 28)   # Giảm kích thước font thông tin tàu vũ trụ
    font_description = pygame.font.Font(None, 20)  # Giảm kích thước font mô tả
    font_instruction = pygame.font.Font(None, 24)  # Giảm kích thước font hướng dẫn

    while True:
        # Vẽ nền gradient
        draw_gradient(screen, black, dark_blue)

        # Hiển thị tiêu đề
        title = "CHOOSE YOUR SPACESHIP"
        title_surface = font_title.render(title, True, yellow)
        title_rect = title_surface.get_rect(center=(screen.get_width() / 2, 40))  # Điều chỉnh vị trí
        screen.blit(title_surface, title_rect)

        # Hiển thị thông tin từng tàu vũ trụ
        for i, spaceship in enumerate(spaceships):
            # Hiệu ứng làm nổi bật tàu vũ trụ được chọn
            if i == selected_index:
                bg_rect = pygame.Rect(80, 100 + i * 120, 740, 100)
                pygame.draw.rect(screen, (50, 50, 100), bg_rect, border_radius=10)  # Nền mờ
                pygame.draw.rect(screen, border_color, bg_rect, 3, border_radius=10)  # Viền phát sáng

            color = neon_blue if i == selected_index else white

            # Vẽ thông tin máy bay
            name_surface = font_info.render(spaceship["name"], True, color)
            name_rect = name_surface.get_rect(topleft=(120, 110 + i * 120))  # Điều chỉnh vị trí
            screen.blit(name_surface, name_rect)

            description_surface = font_description.render(
                f"HP: {spaceship['hp']}  |  Damage: {spaceship['damage']}  |  Speed: {spaceship['speed']}",
                True,
                color,
            )
            description_rect = description_surface.get_rect(topleft=(120, 150 + i * 120))  # Điều chỉnh vị trí
            screen.blit(description_surface, description_rect)

            # Hiển thị hình ảnh tàu vũ trụ với hiệu ứng phóng to nếu được chọn
            spaceship_image = pygame.image.load(spaceship["image"]).convert_alpha()
            if i == selected_index:
                spaceship_image = pygame.transform.scale(spaceship_image, (120, 120))  # Điều chỉnh kích thước
                screen.blit(spaceship_image, (620, 100 + i * 120 - 10))  # Điều chỉnh vị trí
            else:
                spaceship_image = pygame.transform.scale(spaceship_image, (80, 80))  # Điều chỉnh kích thước
                screen.blit(spaceship_image, (640, 110 + i * 120))  # Điều chỉnh vị trí

        # Hiển thị hướng dẫn điều khiển
        instruction_surface = font_instruction.render("Press UP/DOWN to navigate", True, light_blue)
        instruction_rect = instruction_surface.get_rect(center=(screen.get_width() / 2, 460))  # Điều chỉnh vị trí
        screen.blit(instruction_surface, instruction_rect)

        instruction_surface = font_instruction.render("Press ENTER to select", True, light_blue)
        instruction_rect = instruction_surface.get_rect(center=(screen.get_width() / 2, 500))  # Điều chỉnh vị trí
        screen.blit(instruction_surface, instruction_rect)

        # Cập nhật màn hình
        pygame.display.flip()

        # Xử lý sự kiện
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
