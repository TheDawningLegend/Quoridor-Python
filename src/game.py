from collections import deque
from entities.board import Board
from game_config import GameConfig
from entities.player import Player
from settings import *
from entities.wall import WallOrientation, Wall


class Game:
    def __init__(self, config: GameConfig):
        self.config = config
        self.reset()

    def reset(self):
        self.board = Board()

        self.init_players()
        self.current_player_index = 0

        self.walls = []
        self.blocked_edges = set()

        self.game_over = False
        self.winner = None

    def init_players(self):
        if self.config.player_count == 2:
            self.players = [
                Player(4, 0, (0, 120, 255), goal_rows=[8]),
                Player(4, 8, (255, 80, 80), goal_rows=[0]),
            ]
        elif self.config.player_count == 4:
            self.players = [
                Player(4, 0, (0, 120, 255), goal_rows=[8]),
                Player(4, 8, (255, 80, 80), goal_rows=[0]),
                Player(0, 4, (80, 200, 80), goal_rows=[8]),
                Player(8, 4, (200, 180, 60), goal_rows=[0]),
            ]

    def current_player(self):
        return self.players[self.current_player_index]

    def switch_turn(self):
        self.current_player_index = (self.current_player_index + 1) % len(self.players)

    def get_neighbors(self, row, col):
        neighbors = []

        directions = [
            (-1, 0),
            (1, 0),
            (0, -1),
            (0, 1)
        ]

        for dr, dc in directions:
            new_row = row + dr
            new_col = col + dc

            if not (
                0 <= new_row < BOARD_SIZE and
                0 <= new_col < BOARD_SIZE
            ):
                continue

            if self.is_edge_blocked(
                (row, col),
                (new_row, new_col)
            ):
                continue

            neighbors.append((new_row, new_col))

        return neighbors

    def get_opponent(self, player: Player):
        for p in self.players:
            if p is not player:
                return p

        return None

    def get_valid_moves(self, player: Player):
        valid_moves = []

        opponent = self.get_opponent(player)

        neighbors = self.get_neighbors(
            player.row,
            player.col
        )

        for neighbor_row, neighbor_col in neighbors:
            if (
                neighbor_row != opponent.row or
                neighbor_col != opponent.col
            ):
                valid_moves.append(
                    (neighbor_row, neighbor_col)
                )

                continue

            row_direction = neighbor_row - player.row
            col_direction = neighbor_col - player.col

            jump_row = neighbor_row + row_direction
            jump_col = neighbor_col + col_direction

            if (
                0 <= jump_row < BOARD_SIZE and
                0 <= jump_col < BOARD_SIZE and
                not self.is_edge_blocked(
                    (neighbor_row, neighbor_col),
                    (jump_row, jump_col)
                )
            ):
                valid_moves.append(
                    (jump_row, jump_col)
                )

            else:
                if row_direction != 0:
                    diagonal_directions = [
                        (0, -1),
                        (0, 1)
                    ]
                else:
                    diagonal_directions = [
                        (-1, 0),
                        (1, 0)
                    ]

                for diagonal_row_direction, diagonal_col_direction in diagonal_directions:
                    diagonal_row = (
                        neighbor_row +
                        diagonal_row_direction
                    )

                    diagonal_col = (
                        neighbor_col +
                        diagonal_col_direction
                    )

                    if not (
                        0 <= diagonal_row < BOARD_SIZE and
                        0 <= diagonal_col < BOARD_SIZE
                    ):
                        continue

                    if self.is_edge_blocked(
                        (neighbor_row, neighbor_col),
                        (diagonal_row, diagonal_col)
                    ):
                        continue

                    valid_moves.append(
                        (diagonal_row, diagonal_col)
                    )

        return valid_moves

    def can_reach_goal(self, player: Player):
        visited = set()
        queue = deque()

        queue.append((player.row, player.col))
        visited.add((player.row, player.col))

        while queue:
            row, col = queue.popleft()

            if player == self.players[0] and row == BOARD_SIZE - 1:
                return True
            if player == self.players[1] and row == 0:
                return True

            for neighbor in self.get_neighbors(row, col):
                if neighbor in visited:
                    continue

                visited.add(neighbor)
                queue.append(neighbor)

        return False

    def get_wall_segments(self, wall: Wall):
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

    def wall_overlaps(self, new_wall):
        new_segments = self.get_wall_segments(new_wall)

        for wall in self.walls:
            if self.get_wall_segments(wall) & new_segments:
                return True

        return False

    def is_valid_wall(self, orientation, row, col):
        if not (
            0 <= row < BOARD_SIZE - 1 and
            0 <= col < BOARD_SIZE - 1
        ):
            return False

        new_wall = Wall(row, col, orientation)

        if self.wall_overlaps(new_wall):
            return False

        if self.wall_crosses(new_wall):
            return False

        blocked_edges = new_wall.get_blocked_edges()

        for edge in blocked_edges:
            self.block_edge(edge[0], edge[1])

        valid = self.paths_exist()

        for edge in blocked_edges:
            self.unblock_edge(edge[0], edge[1])

        return valid

    def wall_crosses(self, new_wall):
        for wall in self.walls:
            if (
                wall.row == new_wall.row and
                wall.col == new_wall.col and
                wall.orientation != new_wall.orientation
            ):
                return True

        return False

    def paths_exist(self):
        return all(self.can_reach_goal(player) for player in self.players)

    def block_edge(self, cell1, cell2):
        edge = frozenset([cell1, cell2])
        self.blocked_edges.add(edge)

    def unblock_edge(self, cell1, cell2):
        edge = frozenset([cell1, cell2])
        self.blocked_edges.discard(edge)

    def is_edge_blocked(self, cell1, cell2):
        edge = frozenset([cell1, cell2])
        return edge in self.blocked_edges