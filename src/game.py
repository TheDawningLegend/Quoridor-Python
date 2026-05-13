from collections import deque
from enum import Enum

from entities.board import Board
from entities.player import Player
from settings import *
from entities.wall import WallOrientation, Wall


class GameState(Enum):
    MAIN_MENU = 0
    PLAYING = 1


class GameConfig:
    def __init__(self, player_count=2):
        self.player_count = player_count


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
            walls = 10
            self.players = [
                Player(0, 4, BLUE, name="Blue", goal_rows=[8], walls=walls, is_ai=False),
                Player(8, 4, RED, name="Red", goal_rows=[0], walls=walls, is_ai=True),
            ]
        elif self.config.player_count == 4:
            walls = 5
            self.players = [
                Player(0, 4, BLUE, name="Blue", goal_rows=[8], walls=walls, is_ai=False),
                Player(8, 4, RED, name="Red", goal_rows=[0], walls=walls, is_ai=True),
                Player(4, 0, GREEN, name="Green", goal_columns=[8], walls=walls, is_ai=True),
                Player(4, 8, YELLOW, name="Yellow", goal_columns=[0], walls=walls, is_ai=True),
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

    def get_valid_moves(self, player: Player):
        valid_moves = []

        neighbors = self.get_neighbors(
            player.row,
            player.col
        )

        occupied = {
            (p.row, p.col): p
            for p in self.players
            if p != player
        }

        for neighbor_row, neighbor_col in neighbors:
            if (neighbor_row, neighbor_col) not in occupied:
                valid_moves.append((neighbor_row, neighbor_col))
                continue

            row_direction = neighbor_row - player.row
            col_direction = neighbor_col - player.col

            jump_row = neighbor_row + row_direction
            jump_col = neighbor_col + col_direction

            if (
                0 <= jump_row < BOARD_SIZE and
                0 <= jump_col < BOARD_SIZE and
                (jump_row, jump_col) not in occupied and
                not self.is_edge_blocked(
                    (neighbor_row, neighbor_col),
                    (jump_row, jump_col)
                )
            ):
                valid_moves.append((jump_row, jump_col))
                continue

            if row_direction != 0:
                diagonal_directions = [(0, -1), (0, 1)]
            else:
                diagonal_directions = [(-1, 0), (1, 0)]

            for dr, dc in diagonal_directions:
                diag_row = neighbor_row + dr
                diag_col = neighbor_col + dc

                if not (
                    0 <= diag_row < BOARD_SIZE and
                    0 <= diag_col < BOARD_SIZE
                ):
                    continue

                if (diag_row, diag_col) in occupied:
                    continue

                if self.is_edge_blocked(
                    (neighbor_row, neighbor_col),
                    (diag_row, diag_col)
                ):
                    continue

                valid_moves.append((diag_row, diag_col))

        return valid_moves

    def can_reach_goal(self, player: Player):
        visited = set()
        queue = deque()

        queue.append((player.row, player.col))
        visited.add((player.row, player.col))

        while queue:
            row, col = queue.popleft()

            if row in player.goal_rows or col in player.goal_columns:
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

    def move_player(self, player: Player, cell):
        valid_moves = self.get_valid_moves(player)

        if cell not in valid_moves:
            return

        player.row = cell[0]
        player.col = cell[1]

        if player.check_win():
            self.game_over = True
            self.winner = player
        else:
            self.switch_turn()

    def place_wall(self, player: Player, orientation, row, col):
        if not player.walls_remaining > 0:
            return

        if not self.is_valid_wall(orientation, row, col):
            return

        new_wall = Wall(row, col, orientation)

        self.walls.append(new_wall)
        for edge in new_wall.get_blocked_edges():
            self.block_edge(edge[0], edge[1])

        player.walls_remaining -= 1
        self.switch_turn()

    def estimate_distance_to_goal(self, player, pos):
        queue = deque([(pos[0], pos[1], 0)])
        visited = set()

        while queue:
            r, c, dist = queue.popleft()

            if r in player.goal_rows:
                return dist
            if c in player.goal_columns:
                return dist

            if (r, c) in visited:
                continue

            visited.add((r, c))

            for nr, nc in self.get_neighbors(r, c):
                if self.is_edge_blocked((r, c), (nr, nc)):
                    continue

                queue.append((nr, nc, dist + 1))

        return 9999

    def get_wall_candidates(self, player):
        candidates = []

        row, col = player.row, player.col

        for r in range(row - 1, row + 2):
            for c in range(col - 1, col + 2):
                if 0 <= r < BOARD_SIZE - 1 and 0 <= c < BOARD_SIZE - 1:
                    candidates.append((r, c))

        return candidates

    def evaluate_position(self, player):
        my_dist = self.estimate_distance_to_goal(
            player,
            (player.row, player.col)
        )

        opponent_dists = [
            self.estimate_distance_to_goal(
                opp,
                (opp.row, opp.col)
            )
            for opp in self.players
            if opp != player
        ]

        closest_opponent = min(opponent_dists)

        return closest_opponent - my_dist

    def get_most_dangerous_opponent(self, player):
        return min(
            (opp for opp in self.players if opp != player),
            key=lambda p: self.estimate_distance_to_goal(p, (p.row, p.col))
        )

    def simulate_wall(self, row, col, orientation):
        wall = Wall(row, col, orientation)
        edges = wall.get_blocked_edges()

        for e in edges:
            self.block_edge(e[0], e[1])

        valid = self.paths_exist()

        for e in edges:
            self.unblock_edge(e[0], e[1])

        return valid

    def ai_choose_action(self, player):
        best_score = float("-inf")
        best_action = None

        for move in self.get_valid_moves(player):
            original = (player.row, player.col)

            player.row, player.col = move

            score = self.evaluate_position(player)

            player.row, player.col = original

            if score > best_score:
                best_score = score
                best_action = ("MOVE", move)

        for r, c in self.get_wall_candidates(player):
            for orientation in [WallOrientation.HORIZONTAL, WallOrientation.VERTICAL]:
                if not self.simulate_wall(r, c, orientation):
                    continue

                edges = Wall(r, c, orientation).get_blocked_edges()

                for e in edges:
                    self.block_edge(e[0], e[1])

                score = self.evaluate_position(player)

                for e in edges:
                    self.unblock_edge(e[0], e[1])

                if score > best_score:
                    best_score = score
                    best_action = ("WALL", (r, c, orientation))

        return best_action