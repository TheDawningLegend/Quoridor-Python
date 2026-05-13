import pygame
from settings import *

class Player:
    def __init__(self, row, col, color, name="Player", goal_rows=None, goal_columns=None, walls=10, is_ai=False):
        self.row = row
        self.col = col
        self.color = color
        self.name = name
        self.goal_rows = goal_rows or []
        self.goal_columns = goal_columns or []
        self.walls_remaining = walls
        self.is_ai = is_ai

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