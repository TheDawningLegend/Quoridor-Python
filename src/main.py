from collections import deque
import pygame
import sys

from game import Game
from wall import Wall, WallOrientation
from settings import *

game = Game()

pygame.init()

# =====================================
# WINDOW
# =====================================

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Quoridor")

clock = pygame.time.Clock()

# =====================================
# HELPERS
# =====================================

def get_valid_moves(player):
    directions = [
        (-1, 0),
        (1, 0),
        (0, -1),
        (0, 1)
    ]

    valid_moves = []

    opponent = None
    for other_player in game.players:
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
            game,
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
                    game,
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
                        game,
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

            x, y = game.board.board_to_screen(row, col)

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
                return (WallOrientation.HORIZONTAL, row, col)
            if v_rect.collidepoint(mouse_x, mouse_y):
                return (WallOrientation.VERTICAL, row, col)

    return None


def get_wall_segments(wall):
    r, c = wall.row, wall.col
    if wall.orientation == WallOrientation.HORIZONTAL:
        return {
            ((r, c), (r + 1, c)),
            ((r, c + 1), (r + 1, c + 1))
        }
    else:
        return {
            ((r, c), (r, c + 1)),
            ((r + 1, c), (r + 1, c + 1))
        }


def wall_overlaps(game, new_wall):
    new_segments = get_wall_segments(new_wall)

    for wall in game.walls:
        if get_wall_segments(wall) & new_segments:
            return True

    return False


def is_valid_wall(game, orientation, row, col):
    if orientation == WallOrientation.HORIZONTAL:
        if row < 0 or row >= BOARD_SIZE - 1:
            return False
        if col < 0 or col >= BOARD_SIZE - 1:
            return False

    elif orientation == WallOrientation.VERTICAL:
        if row < 0 or row >= BOARD_SIZE - 1:
            return False
        if col < 0 or col >= BOARD_SIZE - 1:
            return False

    new_wall = Wall(row, col, orientation)

    return not wall_overlaps(game, new_wall)


def is_blocked(game, start_row, start_col, target_row, target_col):
    if target_row > start_row:
        for wall in game.walls:
            if wall.orientation == WallOrientation.HORIZONTAL:
                if (
                    wall.row == start_row and
                    wall.col in (start_col, start_col - 1)
                ):
                    return True

    elif target_row < start_row:
        for wall in game.walls:
            if wall.orientation == WallOrientation.HORIZONTAL:
                if (
                    wall.row == target_row and
                    wall.col in (target_col, target_col - 1)
                ):
                    return True

    elif target_col > start_col:
        for wall in game.walls:
            if wall.orientation == WallOrientation.VERTICAL:
                if (
                    wall.col == start_col and
                    wall.row in (start_row, start_row - 1)
                ):
                    return True

    elif target_col < start_col:
        for wall in game.walls:
            if wall.orientation == WallOrientation.VERTICAL:
                if (
                    wall.col == target_col and
                    wall.row in (target_row, target_row - 1)
                ):
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

        if player == game.player1 and row == 8:
            return True
        if player == game.player2 and row == 0:
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
                game,
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
        can_reach_goal(game.player1) and
        can_reach_goal(game.player2)
    )

# =====================================
# DRAWING
# =====================================

def draw_valid_moves(player):
    valid_moves = get_valid_moves(player)

    for row, col in valid_moves:
        x, y = game.board.board_to_screen(row, col)

        highlight_rect = pygame.Rect(
            x + 10,
            y + 10,
            CELL_SIZE - 20,
            CELL_SIZE - 20
        )

        pygame.draw.rect(screen, HIGHLIGHT_COLOR, highlight_rect)


def draw_winner():
    if not game.game_over:
        return

    if game.winner == game.player1:
        text = "Blue Player Wins!"
    else:
        text = "Red Player Wins!"

    surface = font.render(
        text + "  (Press R to Restart)",
        True,
        (255, 255, 255)
    )

    rect = surface.get_rect(
        center=(WINDOW_WIDTH // 2, 50)
    )

    screen.blit(surface, rect)

# =====================================
# MAIN LOOP
# =====================================

running = True
font = pygame.font.SysFont(None, 48)
wall_mode = False

while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                wall_mode = not wall_mode

            if event.key == pygame.K_r:
                game.reset()

        if (
            event.type == pygame.MOUSEBUTTONDOWN and
            not game.game_over
        ):
            mouse_x, mouse_y = pygame.mouse.get_pos()

            clicked_cell = game.board.screen_to_board(mouse_x, mouse_y)

            if clicked_cell:
                current_player = game.current_player()
                valid_moves = get_valid_moves(current_player)

                if clicked_cell in valid_moves:
                    current_player.row = clicked_cell[0]
                    current_player.col = clicked_cell[1]

                    if current_player == game.player1:
                        if current_player.row == BOARD_SIZE - 1:
                            game.game_over = True
                            game.winner = game.player1
                    elif current_player == game.player2:
                        if current_player.row == 0:
                            game.game_over = True
                            game.winner = game.player2

                    game.switch_turn()

            if wall_mode:
                current_player = game.current_player()

                if current_player.walls_remaining > 0:
                    result = get_wall_position(mouse_x, mouse_y)

                    if result:
                        orientation, row, col = result

                        if is_valid_wall(game, orientation, row, col):
                            new_wall = Wall(row, col, orientation)
                            game.walls.append(new_wall)

                            if paths_exist():
                                current_player.walls_remaining -= 1
                                game.switch_turn()
                            else:
                                game.walls.remove(new_wall)

    screen.fill(BACKGROUND_COLOR)

    game.board.draw(screen, game.board)
    draw_valid_moves(game.current_player())
    draw_winner()
    for wall in game.walls:
        wall.draw(screen, game.board)
    for player in game.players:
        player.draw(screen, game.board)

    pygame.display.flip()

pygame.quit()
sys.exit()