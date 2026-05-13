import pygame
from settings import *
from drawable import Drawable

class Board(Drawable):
    def board_to_screen(self, row, col):
        x = BOARD_OFFSET_X + col * (CELL_SIZE + WALL_SIZE)
        y = BOARD_OFFSET_Y + row * (CELL_SIZE + WALL_SIZE)

        return x, y

    def screen_to_board(self, mouse_x, mouse_y):
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):

                x, y = self.board_to_screen(row, col)

                rect = pygame.Rect(
                    x,
                    y,
                    CELL_SIZE,
                    CELL_SIZE
                )

                if rect.collidepoint(mouse_x, mouse_y):
                    return row, col

        return None

    def draw(self, screen, board=None):
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):

                x, y = self.board_to_screen(row, col)

                rect = pygame.Rect(
                    x,
                    y,
                    CELL_SIZE,
                    CELL_SIZE
                )

                pygame.draw.rect(
                    screen,
                    CELL_COLOR,
                    rect
                )