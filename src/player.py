class Player:
    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.color = color
        self.walls_remaining = 10