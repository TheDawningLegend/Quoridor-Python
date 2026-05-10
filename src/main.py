import pygame
import sys

pygame.init()

# =====================================
# WINDOW
# =====================================

WINDOW_WIDTH = 900
WINDOW_HEIGHT = 900

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Quoridor")

clock = pygame.time.Clock()
FPS = 60

# =====================================
# BOARD SETTINGS
# =====================================

BOARD_SIZE = 9

CELL_SIZE = 70
WALL_SIZE = 12

BOARD_PIXEL_SIZE = (
    BOARD_SIZE * CELL_SIZE +
    (BOARD_SIZE - 1) * WALL_SIZE
)

BOARD_OFFSET_X = (WINDOW_WIDTH - BOARD_PIXEL_SIZE) // 2
BOARD_OFFSET_Y = (WINDOW_HEIGHT - BOARD_PIXEL_SIZE) // 2

# =====================================
# COLORS
# =====================================

BACKGROUND_COLOR = (40, 40, 40)
CELL_COLOR = (240, 220, 170)

BLUE = (70, 120, 255)
RED = (220, 70, 70)

# =====================================
# PLAYER
# =====================================

class Player:
    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.color = color

player1 = Player(0, 4, BLUE)
player2 = Player(8, 4, RED)

# =====================================
# HELPERS
# =====================================

def board_to_screen(row, col):
    x = BOARD_OFFSET_X + col * (CELL_SIZE + WALL_SIZE)
    y = BOARD_OFFSET_Y + row * (CELL_SIZE + WALL_SIZE)

    return x, y

# =====================================
# DRAWING
# =====================================

def draw_board():
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):

            x = BOARD_OFFSET_X + col * (CELL_SIZE + WALL_SIZE)
            y = BOARD_OFFSET_Y + row * (CELL_SIZE + WALL_SIZE)

            rect = pygame.Rect(
                x,
                y,
                CELL_SIZE,
                CELL_SIZE
            )

            pygame.draw.rect(screen, CELL_COLOR, rect)

def draw_player(player):
    x, y = board_to_screen(player.row, player.col)

    center_x = x + CELL_SIZE // 2
    center_y = y + CELL_SIZE // 2

    pygame.draw.circle(
        screen,
        player.color,
        (center_x, center_y),
        CELL_SIZE // 3
    )

# =====================================
# MAIN LOOP
# =====================================

running = True

while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(BACKGROUND_COLOR)

    draw_board()
    draw_player(player1)
    draw_player(player2)

    pygame.display.flip()

pygame.quit()
sys.exit()