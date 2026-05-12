import pygame
import sys

from game import Game
from player import Player
from wall import Wall, WallOrientation
from settings import *

game = Game()

pygame.init()
pygame.display.set_caption("Quoridor")
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pygame.time.Clock()

# =====================================
# HELPERS
# =====================================

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
                return WallOrientation.HORIZONTAL, row, col
            if v_rect.collidepoint(mouse_x, mouse_y):
                return WallOrientation.VERTICAL, row, col

    return None

# =====================================
# DRAWING
# =====================================

font = pygame.font.SysFont(None, 48)
ui_font = pygame.font.SysFont(None, 32)
ui_small_font = pygame.font.SysFont(None, 24)

def draw_valid_moves(player: Player):
    valid_moves = game.get_valid_moves(player)

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


def draw_wall_preview():
    mouse_x, mouse_y = pygame.mouse.get_pos()

    result = get_wall_position(mouse_x, mouse_y)

    if not result:
        return

    orientation, row, col = result

    valid = game.is_valid_wall(
        orientation,
        row,
        col
    )

    color = (
        VALID_PREVIEW_COLOR
        if valid
        else INVALID_PREVIEW_COLOR
    )

    x, y = game.board.board_to_screen(row, col)

    if orientation == WallOrientation.HORIZONTAL:
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

    preview_surface = pygame.Surface(
        (rect.width, rect.height),
        pygame.SRCALPHA
    )

    preview_surface.fill((*color, 160))

    screen.blit(
        preview_surface,
        (rect.x, rect.y)
    )


def draw_player_panel(x, y, width, height, title, player, is_active):
    rect = pygame.Rect(x, y, width, height)

    pygame.draw.rect(
        screen,
        UI_PANEL_COLOR,
        rect,
        border_radius=10
    )

    padding_x = x + 8
    padding_y = y + 8

    title_surface = ui_font.render(
        title,
        True,
        player.color
    )

    walls_surface = ui_small_font.render(
        f"Walls: {player.walls_remaining}",
        True,
        UI_TEXT_COLOR
    )

    screen.blit(title_surface, (padding_x, padding_y))
    screen.blit(walls_surface, (padding_x, padding_y + 30))

    if is_active:
        turn_surface = ui_small_font.render(
            "YOUR TURN",
            True,
            (120, 220, 120)
        )

        screen.blit(turn_surface, (padding_x + 100, padding_y + 30))


def draw_ui():
    panel_width = 220
    panel_height = 64
    margin = 8

    draw_player_panel(
        margin,
        margin,
        panel_width,
        panel_height,
        "Blue Player",
        game.player1,
        game.current_player() == game.player1
    )

    draw_player_panel(
        WINDOW_WIDTH - panel_width - margin,
        WINDOW_HEIGHT - panel_height - margin,
        panel_width,
        panel_height,
        "Red Player",
        game.player2,
        game.current_player() == game.player2
    )

    controls_surface = ui_small_font.render(
        "[R] Restart",
        True,
        (180, 180, 180)
    )

    screen.blit(
        controls_surface,
        (margin, WINDOW_HEIGHT - 35)
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

        if event.type == pygame.KEYDOWN:
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
                valid_moves = game.get_valid_moves(current_player)

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

            current_player = game.current_player()

            if current_player.walls_remaining > 0:
                result = get_wall_position(mouse_x, mouse_y)

                if result:
                    orientation, row, col = result

                    if game.is_valid_wall(orientation, row, col):
                        new_wall = Wall(row, col, orientation)

                        game.walls.append(new_wall)
                        for edge in new_wall.get_blocked_edges():
                            game.block_edge(edge[0], edge[1])

                        current_player.walls_remaining -= 1
                        game.switch_turn()

    screen.fill(BACKGROUND_COLOR)

    game.board.draw(screen, game.board)
    draw_valid_moves(game.current_player())
    draw_wall_preview()
    for wall in game.walls:
        wall.draw(screen, game.board)
    for player in game.players:
        player.draw(screen, game.board)
    draw_ui()
    draw_winner()

    pygame.display.flip()

pygame.quit()
sys.exit()