import pygame
from game import Game
from constants import *

if __name__ == "__main__":
    pygame.init()

    # Tao cua so
    screen = pygame.display.set_mode((screen_width, screen_height))

    # Khoi tao tien trinh game
    game = Game()

    # Chay game
    game.run(screen)

    # Thoat game
    pygame.quit()
