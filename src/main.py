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

HIGHLIGHT_COLOR = (120, 255, 120)

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

players = [player1, player2]

current_player_index = 0

# =====================================
# HELPERS
# =====================================

def board_to_screen(row, col):
    x = BOARD_OFFSET_X + col * (CELL_SIZE + WALL_SIZE)
    y = BOARD_OFFSET_Y + row * (CELL_SIZE + WALL_SIZE)

    return x, y


def screen_to_board(mouse_x, mouse_y):
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):

            x, y = board_to_screen(row, col)

            rect = pygame.Rect(
                x,
                y,
                CELL_SIZE,
                CELL_SIZE
            )

            if rect.collidepoint(mouse_x, mouse_y):
                return row, col

    return None


def get_valid_moves(player):
    directions = [
        (-1, 0),
        (1, 0),
        (0, -1),
        (0, 1)
    ]

    valid_moves = []

    for dr, dc in directions:
        new_row = player.row + dr
        new_col = player.col + dc

        if (
            0 <= new_row < BOARD_SIZE and
            0 <= new_col < BOARD_SIZE
        ):
            occupied = False

            for other in players:
                if other != player:
                    if other.row == new_row and other.col == new_col:
                        occupied = True

            if not occupied:
                valid_moves.append((new_row, new_col))

    return valid_moves

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


def draw_valid_moves(player):
    valid_moves = get_valid_moves(player)

    for row, col in valid_moves:
        x, y = board_to_screen(row, col)

        highlight_rect = pygame.Rect(
            x + 10,
            y + 10,
            CELL_SIZE - 20,
            CELL_SIZE - 20
        )

        pygame.draw.rect(screen, HIGHLIGHT_COLOR, highlight_rect)

# =====================================
# MAIN LOOP
# =====================================

running = True

while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()

            clicked_cell = screen_to_board(mouse_x, mouse_y)

            if clicked_cell:
                current_player = players[current_player_index]
                valid_moves = get_valid_moves(current_player)

                if clicked_cell in valid_moves:
                    current_player.row = clicked_cell[0]
                    current_player.col = clicked_cell[1]

                    current_player_index = (current_player_index + 1) % 2

    screen.fill(BACKGROUND_COLOR)

    draw_board()

    draw_valid_moves(players[current_player_index])

    for player in players:
        draw_player(player)

    pygame.display.flip()

pygame.quit()
sys.exit()