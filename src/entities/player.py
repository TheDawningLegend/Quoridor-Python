import pygame
from settings import *
from drawable import Drawable

class Player(Drawable):
    def __init__(self, row, col, color, goal_rows=None, goal_columns=None):
        self.row = row
        self.col = col
        self.color = color
        self.walls_remaining = 10
        self.goal_rows = goal_rows or []
        self.goal_columns = goal_columns or []

    def check_win(self):
        return self.row in self.goal_rows or self.col in self.goal_columns

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