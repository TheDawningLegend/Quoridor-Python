# =====================================
# WINDOW
# =====================================

WINDOW_WIDTH = 900
WINDOW_HEIGHT = 900
FPS = 60

# =====================================
# BOARD
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