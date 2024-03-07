from typ import Point

WINDOW_DESC = "The Witness"

DEBUG = True  # Must be True for tests to pass

RIGHT: Point = (1, 0)
UP: Point = (0, 1)
LEFT: Point = (-1, 0)
DOWN: Point = (0, -1)

BLACK = (0, 0, 0)
CELL_BACK = (1, 41, 31)
CELL_WHITE = (215, 218, 216)
BORDER_GREEN = (7, 60, 52)
LINE_GREEN = (27, 47, 56)
INNER_CELL_GREEN = (0, 164, 130)
BACKGROUND_BROWN = (37, 21, 3)
PALETTE_COLORS = (
        BLACK +
        CELL_BACK +
        CELL_WHITE +
        BORDER_GREEN +
        LINE_GREEN +
        INNER_CELL_GREEN +
        BACKGROUND_BROWN
)