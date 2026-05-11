from enum import Enum
import pygame
from settings import *
from drawable import Drawable


class WallOrientation(Enum):
    HORIZONTAL = 0
    VERTICAL = 1


class Wall(Drawable):
    def __init__(self, row, col, orientation: WallOrientation):
        self.row = row
        self.col = col
        self.orientation = orientation

    def get_blocked_edges(self):
        r = self.row
        c = self.col

        if self.orientation == WallOrientation.HORIZONTAL:
            return [
                ((r, c), (r + 1, c)),
                ((r, c + 1), (r + 1, c + 1))
            ]
        else:
            return [
                ((r, c), (r, c + 1)),
                ((r + 1, c), (r + 1, c + 1))
            ]

    def draw(self, screen, board):
        x, y = board.board_to_screen(self.row, self.col)

        if self.orientation == WallOrientation.HORIZONTAL:
            rect = pygame.Rect(
                x,
                y + CELL_SIZE,
                CELL_SIZE * 2 + WALL_SIZE,
                WALL_SIZE
            )
        else:
            rect = pygame.Rect(
                x + CELL_SIZE,
                y,
                WALL_SIZE,
                CELL_SIZE * 2 + WALL_SIZE
            )

        pygame.draw.rect(
            screen,
            WALL_COLOR,
            rect
        )