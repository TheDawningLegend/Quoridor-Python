import pygame
from settings import *
from drawable import Drawable

class Player(Drawable):
    def __init__(self, row, col, color, goal_rows=None):
        self.row = row
        self.col = col
        self.color = color
        self.walls_remaining = 10
        self.goal_rows = goal_rows or []

    def draw(self, screen, board):
        x, y = board.board_to_screen(self.row, self.col)

        center = (
            x + CELL_SIZE // 2,
            y + CELL_SIZE // 2
        )

        pygame.draw.circle(
            screen,
            self.color,
            center,
            CELL_SIZE // 3
        )