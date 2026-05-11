from collections import deque
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
WALL_COLOR = (200, 200, 200)

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
        self.walls_remaining = 10


player1 = Player(0, 4, BLUE)
player2 = Player(8, 4, RED)

players = [player1, player2]

current_player_index = 0

horizontal_walls = set()
vertical_walls = set()

wall_mode = False

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

    opponent = None
    for other_player in players:
        if other_player != player:
            opponent = other_player
            break

    for row_offset, col_offset in directions:
        adjacent_row = player.row + row_offset
        adjacent_col = player.col + col_offset

        if not (
            0 <= adjacent_row < BOARD_SIZE and
            0 <= adjacent_col < BOARD_SIZE
        ):
            continue

        if is_blocked(
            player.row,
            player.col,
            adjacent_row,
            adjacent_col
        ):
            continue

        if (
                adjacent_row == opponent.row and
                adjacent_col == opponent.col
        ):
            jump_row = adjacent_row + row_offset
            jump_col = adjacent_col + col_offset

            can_jump_straight = False

            if (
                    0 <= jump_row < BOARD_SIZE and
                    0 <= jump_col < BOARD_SIZE
            ):
                if not is_blocked(
                        adjacent_row,
                        adjacent_col,
                        jump_row,
                        jump_col
                ):
                    can_jump_straight = True

                    valid_moves.append(
                        (jump_row, jump_col)
                    )

            if not can_jump_straight:
                if row_offset != 0:
                    diagonal_directions = [
                        (0, -1),
                        (0, 1)
                    ]
                else:
                    diagonal_directions = [
                        (-1, 0),
                        (1, 0)
                    ]

                for diagonal_row_offset, diagonal_col_offset in diagonal_directions:
                    diagonal_row = (
                            adjacent_row +
                            diagonal_row_offset
                    )

                    diagonal_col = (
                            adjacent_col +
                            diagonal_col_offset
                    )

                    if not (
                            0 <= diagonal_row < BOARD_SIZE and
                            0 <= diagonal_col < BOARD_SIZE
                    ):
                        continue

                    if is_blocked(
                            adjacent_row,
                            adjacent_col,
                            diagonal_row,
                            diagonal_col
                    ):
                        continue

                    valid_moves.append(
                        (diagonal_row, diagonal_col)
                    )

            continue

        valid_moves.append(
            (adjacent_row, adjacent_col)
        )

    return valid_moves


def get_wall_position(mouse_x, mouse_y):
    for row in range(BOARD_SIZE - 1):
        for col in range(BOARD_SIZE - 1):

            x, y = board_to_screen(row, col)

            h_rect = pygame.Rect(
                x,
                y + CELL_SIZE,
                CELL_SIZE * 2 + WALL_SIZE,
                WALL_SIZE
            )

            v_rect = pygame.Rect(
                x + CELL_SIZE,
                y,
                WALL_SIZE,
                CELL_SIZE * 2 + WALL_SIZE
            )

            if h_rect.collidepoint(mouse_x, mouse_y):
                return ("H", row, col)
            if v_rect.collidepoint(mouse_x, mouse_y):
                return ("V", row, col)

    return None


def is_valid_wall(direction, row, col):
    if direction == "H":
        if (row, col) in horizontal_walls:
            return False
        if (row, col - 1) in horizontal_walls:
            return False
        if (row, col + 1) in horizontal_walls:
            return False
        if (row, col) in vertical_walls:
            return False

    elif direction == "V":
        if (row, col) in vertical_walls:
            return False
        if (row - 1, col) in vertical_walls:
            return False
        if (row + 1, col) in vertical_walls:
            return False
        if (row, col) in horizontal_walls:
            return False

    return True


def is_blocked(start_row, start_col, target_row, target_col):
    if target_row > start_row:
        if (start_row, start_col) in horizontal_walls:
            return True
        if (start_row, start_col - 1) in horizontal_walls:
            return True

    elif target_row < start_row:
        if (target_row, target_col) in horizontal_walls:
            return True
        if (target_row, target_col - 1) in horizontal_walls:
            return True

    elif target_col > start_col:
        if (start_row, start_col) in vertical_walls:
            return True
        if (start_row - 1, start_col) in vertical_walls:
            return True

    elif target_col < start_col:
        if (target_row, target_col) in vertical_walls:
            return True
        if (target_row - 1, target_col) in vertical_walls:
            return True

    return False


def can_reach_goal(player):
    visited = set()

    queue = deque()
    queue.append((player.row, player.col))

    visited.add((player.row, player.col))

    directions = [
        (-1, 0),
        (1, 0),
        (0, -1),
        (0, 1)
    ]

    while queue:
        row, col = queue.popleft()

        if player == player1 and row == 8:
            return True
        if player == player2 and row == 0:
            return True

        for dr, dc in directions:
            new_row = row + dr
            new_col = col + dc

            if not (
                0 <= new_row < BOARD_SIZE and
                0 <= new_col < BOARD_SIZE
            ):
                continue

            if (new_row, new_col) in visited:
                continue

            if is_blocked(
                row,
                col,
                new_row,
                new_col
            ):
                continue

            visited.add((new_row, new_col))

            queue.append((new_row, new_col))

    return False


def paths_exist():
    return (
        can_reach_goal(player1) and
        can_reach_goal(player2)
    )

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


def draw_walls():
    for row, col in horizontal_walls:
        x, y = board_to_screen(row, col)

        rect = pygame.Rect(
            x,
            y + CELL_SIZE,
            CELL_SIZE * 2 + WALL_SIZE,
            WALL_SIZE
        )

        pygame.draw.rect(screen, WALL_COLOR, rect)

    for row, col in vertical_walls:
        x, y = board_to_screen(row, col)

        rect = pygame.Rect(
            x + CELL_SIZE,
            y,
            WALL_SIZE,
            CELL_SIZE * 2 + WALL_SIZE
        )

        pygame.draw.rect(screen, WALL_COLOR, rect)

# =====================================
# MAIN LOOP
# =====================================

running = True

while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                wall_mode = not wall_mode

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

            if wall_mode:
                current_player = players[current_player_index]

                if current_player.walls_remaining > 0:
                    result = get_wall_position(mouse_x, mouse_y)

                    if result:
                        direction, row, col = result

                        if is_valid_wall(direction, row, col):
                            if direction == "H":
                                horizontal_walls.add((row, col))
                            else:
                                vertical_walls.add((row, col))

                            if paths_exist():
                                current_player.walls_remaining -= 1
                                current_player_index = (current_player_index + 1) % 2
                            else:
                                if direction == "H":
                                    horizontal_walls.remove((row, col))
                                else:
                                    vertical_walls.remove((row, col))

    screen.fill(BACKGROUND_COLOR)

    draw_board()
    draw_walls()
    draw_valid_moves(players[current_player_index])

    for player in players:
        draw_player(player)

    pygame.display.flip()

pygame.quit()
sys.exit()