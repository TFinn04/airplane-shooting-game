import pygame
from game import Game
from constants import *

if __name__ == "__main__":
    pygame.init()

    # Tạo cửa sổ
    screen = pygame.display.set_mode((screen_width, screen_height))

    # Khởi động tiến trình
    game = Game()

    # Chạy game
    game.game_loop(screen)

    # Thoát
    pygame.quit()
