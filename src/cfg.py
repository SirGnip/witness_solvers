from typ import Point

DEBUG = True  # Must be True for tests to pass

WINDOW_DESC = "The Witness"

RIGHT: Point = (1, 0)
UP: Point = (0, 1)
LEFT: Point = (-1, 0)
DOWN: Point = (0, -1)

BLACK = (0, 0, 0)
CELL_BLACK = (1, 41, 31)
CELL_WHITE = (215, 218, 216)
BORDER_GREEN = (7, 60, 52)
LINE_GREEN = (27, 47, 56)
INNER_CELL_GREEN = (0, 164, 130)
BACKGROUND_BROWN = (37, 21, 3)
PALETTE_COLORS = (
        BLACK +
        CELL_BLACK +
        CELL_WHITE +
        BORDER_GREEN +
        LINE_GREEN +
        INNER_CELL_GREEN +
        BACKGROUND_BROWN
)

(
    BLACK_IDX,
    CELL_BLACK_IDX,
    CELL_WHITE_IDX,
    BORDER_GREEN_IDX,
    LINE_GREEN_IDX,
    INNER_CELL_GREEN_IDX,
    BACKGROUND_BROWN_IDX
) = range(7)

DEBUG_COLOR_IDX = CELL_WHITE_IDX


PANEL_BOUNDING_BOX_WHISKER_START_X = (260, 380)
PANEL_BOUNDING_BOX_WHISKER_START_Y = (180, 300)

if DEBUG:
    EMPTY, START, END, INTERSECT, HORIZ_ON, HORIZ_OFF, VERT_ON, VERT_OFF = ' O^+X-X|'  # good for debugging grid/path
else:
    # EMPTY, START, END, INTERSECT, HORIZ_ON, HORIZ_OFF, VERT_ON, VERT_OFF = ' O^ ━ ┃ '  # good for showing solutions
    # EMPTY, START, END, INTERSECT, HORIZ_ON, HORIZ_OFF, VERT_ON, VERT_OFF =   ' O^ ═-║|'  # good for showing solutions
    EMPTY, START, END, INTERSECT, HORIZ_ON, HORIZ_OFF, VERT_ON, VERT_OFF = ' O^ ━-┃|'  # good for showing solutions
