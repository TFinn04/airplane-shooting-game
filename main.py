import pygame
import os
import time
from game import Game
from high_score_manager import HighScoreManager
from constants import *


# Khởi tạo mixer
pygame.mixer.init()

# Tải và phát nhạc nền
pygame.mixer.music.load("Sounds/club.mp3")  # Đường dẫn tới tệp nhạc của bạn
pygame.mixer.music.play(-1)  # Phát lặp vô hạn
pygame.mixer.music.set_volume(0.2)  # Điều chỉnh âm lượng (0.0 - 1.0)


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
    font_info = pygame.font.Font(None, 28)  # Giảm kích thước font thông tin tàu vũ trụ
    font_description = pygame.font.Font(None, 20)  # Giảm kích thước font mô tả
    font_instruction = pygame.font.Font(None, 24)  # Giảm kích thước font hướng dẫn

    while True:
        # Vẽ nền gradient
        draw_gradient(screen, black, dark_blue)

        # Hiển thị tiêu đề
        title = "CHOOSE YOUR SPACESHIP"
        title_surface = font_title.render(title, True, yellow)
        title_rect = title_surface.get_rect(
            center=(screen.get_width() / 2, 40)
        )  # Điều chỉnh vị trí
        screen.blit(title_surface, title_rect)

        # Hiển thị thông tin từng tàu vũ trụ
        for i, spaceship in enumerate(spaceships):
            # Hiệu ứng làm nổi bật tàu vũ trụ được chọn
            if i == selected_index:
                bg_rect = pygame.Rect(80, 100 + i * 120, 740, 100)
                pygame.draw.rect(
                    screen, (50, 50, 100), bg_rect, border_radius=10
                )  # Nền mờ
                pygame.draw.rect(
                    screen, border_color, bg_rect, 3, border_radius=10
                )  # Viền phát sáng

            color = neon_blue if i == selected_index else white

            # Vẽ thông tin máy bay
            name_surface = font_info.render(spaceship["name"], True, color)
            name_rect = name_surface.get_rect(
                topleft=(120, 110 + i * 120)
            )  # Điều chỉnh vị trí
            screen.blit(name_surface, name_rect)

            description_surface = font_description.render(
                f"HP: {spaceship['hp']}  |  Damage: {spaceship['damage']}  |  Speed: {spaceship['speed']}",
                True,
                color,
            )
            description_rect = description_surface.get_rect(
                topleft=(120, 150 + i * 120)
            )  # Điều chỉnh vị trí
            screen.blit(description_surface, description_rect)

            # Hiển thị hình ảnh tàu vũ trụ với hiệu ứng phóng to nếu được chọn
            spaceship_image = pygame.image.load(
                os.path.join(spaceship["image_folder"], "player1.png")
            ).convert_alpha()
            if i == selected_index:
                spaceship_image = pygame.transform.scale(
                    spaceship_image, (120, 120)
                )  # Điều chỉnh kích thước
                screen.blit(
                    spaceship_image, (620, 100 + i * 120 - 10)
                )  # Điều chỉnh vị trí
            else:
                spaceship_image = pygame.transform.scale(
                    spaceship_image, (80, 80)
                )  # Điều chỉnh kích thước
                screen.blit(spaceship_image, (640, 110 + i * 120))  # Điều chỉnh vị trí

        # Hiển thị hướng dẫn điều khiển
        instruction_surface = font_instruction.render(
            "Press UP/DOWN to navigate", True, light_blue
        )
        instruction_rect = instruction_surface.get_rect(
            center=(screen.get_width() / 2, 460)
        )  # Điều chỉnh vị trí
        screen.blit(instruction_surface, instruction_rect)

        instruction_surface = font_instruction.render(
            "Press ENTER to select", True, light_blue
        )
        instruction_rect = instruction_surface.get_rect(
            center=(screen.get_width() / 2, 500)
        )  # Điều chỉnh vị trí
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

def load_images_from_folder(folder_path):
    images = []
    for filename in sorted(os.listdir(folder_path), key=lambda x: int(x[4:-4])):
        if filename.endswith(".png"):  # Load file ảnh có định dạng .png
            image_path = os.path.join(folder_path, filename)
            images.append(pygame.image.load(image_path).convert_alpha())
    return images

def main_menu(screen, high_score_manager):
    # Load the menu background animation frames
    background_frames = load_images_from_folder("Images/menu")
    frame_index = 0
    last_update_time = time.time()  # Lưu thời gian frame cuối cùng được cập nhật
    frame_delay = 0.04  # Độ trễ giữa các frame (tính bằng giây)

    # Load custom font for a more modern style
    try:
        font_path = "Fonts/orbitron.ttf"
        title_font = pygame.font.Font(font_path, 80)
        option_font = pygame.font.Font(font_path, 40)
    except FileNotFoundError:
        title_font = pygame.font.SysFont("Arial", 70, bold=True)
        option_font = pygame.font.SysFont("Arial", 30, bold=True)

    selected_option = 0  # Track the currently selected menu option
    menu_options = ["Play", "Show High Score", "Reset High Score", "Exit"]

    while True:
        # Update animation frame
        current_time = time.time()
        if current_time - last_update_time > frame_delay:
            frame_index = (frame_index + 1) % len(background_frames)
            last_update_time = current_time

        # Draw animated background
        screen.blit(
            pygame.transform.scale(
                background_frames[frame_index], (screen_width, screen_height)
            ),
            (0, 0),
        )

        # Draw title
        title_surface = title_font.render("SPACE SHOOTER", True, (255, 223, 0))
        title_rect = title_surface.get_rect(center=(screen_width // 2, 100))
        screen.blit(title_surface, title_rect)

        # Draw menu options
        for i, option in enumerate(menu_options):
            color = (255, 223, 0) if i == selected_option else (200, 200, 200)
            option_surface = option_font.render(option, True, color)
            option_rect = option_surface.get_rect(
                center=(screen_width // 2, 200 + i * 80)
            )
            screen.blit(option_surface, option_rect)

        pygame.display.flip()

        # Handle input for menu navigation
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "exit"
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    selected_option = (selected_option - 1) % len(menu_options)
                elif event.key == pygame.K_DOWN:
                    selected_option = (selected_option + 1) % len(menu_options)
                elif event.key == pygame.K_RETURN:
                    if selected_option == 0:  # Play
                        return "play"
                    elif selected_option == 1:  # Show High Score
                        return "show_high_score"
                    elif selected_option == 2:  # Reset High Score
                        high_score_manager.reset_high_score()
                    elif selected_option == 3:  # Exit
                        return "exit"


def show_high_score(screen, high_score_manager):
    # Load custom font
    try:
        font_path = "Fonts/orbitron.ttf"
        title_font = pygame.font.Font(font_path, 80)
        score_font = pygame.font.Font(font_path, 50)
        instruction_font = pygame.font.Font(font_path, 30)
    except FileNotFoundError:
        title_font = pygame.font.SysFont("Arial", 70, bold=True)
        score_font = pygame.font.SysFont("Arial", 40, bold=True)
        instruction_font = pygame.font.SysFont("Arial", 30, bold=True)

    glow_alpha = 0
    glow_increasing = True

    while True:
        # Fill the screen with a background color
        screen.fill((0, 0, 50))

        # Handle glow animation
        if glow_increasing:
            glow_alpha += 3
            if glow_alpha > 150:
                glow_increasing = False
        else:
            glow_alpha -= 3
            if glow_alpha < 0:
                glow_increasing = True

        # Create a transparent surface for the glowing rectangle
        glow_surface = pygame.Surface(
            (screen.get_width(), screen.get_height()), pygame.SRCALPHA
        )
        glow_color = (255, 223, 0, glow_alpha)  # RGBA with alpha

        # Create rectangle
        title_rect = pygame.Rect(
            screen.get_width() // 2 - 200, 100, 400, 80
        )  # Rect for title
        pygame.draw.rect(
            glow_surface, glow_color[:3], title_rect.inflate(50, 30), border_radius=20
        )

        # Blit the glow surface onto the main screen
        screen.blit(glow_surface, (0, 0))

        # Draw the title
        title_surface = title_font.render("HIGH SCORE", True, (255, 255, 255))
        title_rect = title_surface.get_rect(center=(screen.get_width() // 2, 140))
        screen.blit(title_surface, title_rect)

        # Display the high score
        score_surface = score_font.render(
            f"High Score: {high_score_manager.high_score}", True, (255, 255, 255)
        )
        score_rect = score_surface.get_rect(center=(screen.get_width() // 2, 250))
        screen.blit(score_surface, score_rect)

        # Display instructions
        instruction_surface = instruction_font.render(
            "Press M to return to Main Menu", True, (200, 200, 200)
        )
        instruction_rect = instruction_surface.get_rect(
            center=(screen.get_width() // 2, 350)
        )
        screen.blit(instruction_surface, instruction_rect)

        # Update the screen
        pygame.display.flip()

        # Handle events
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
            result = game.game_loop(
                screen, spaceship_data
            )  # Truyền thông tin máy bay vào game loop
            if result == "exit":
                break
        elif action == "show_high_score":
            result = show_high_score(screen, high_score_manager)
            if result == "exit":
                break
        elif action == "exit":
            break

    pygame.quit() 
