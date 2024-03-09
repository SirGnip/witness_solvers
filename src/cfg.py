from typ import Point

DEBUG = False  # Must be True for tests to pass
SHOW_DEBUG_IMG = True

if DEBUG:
    # good for debugging by showing all edges and intersections
    # EMPTY, START, END, INTERSECT, HORIZ_ON, HORIZ_OFF, VERT_ON, VERT_OFF = ' O^+X-X|'
    EMPTY, START, END, INTERSECT, HORIZ_ON, HORIZ_OFF, VERT_ON, VERT_OFF = ' O^+X-X|'
else:
    # good for showing solutions
    # EMPTY, START, END, INTERSECT, HORIZ_ON, HORIZ_OFF, VERT_ON, VERT_OFF =   ' O^ ═-║|'
    # EMPTY, START, END, INTERSECT, HORIZ_ON, HORIZ_OFF, VERT_ON, VERT_OFF =   ' O^ ═ ║ '
    # EMPTY, START, END, INTERSECT, HORIZ_ON, HORIZ_OFF, VERT_ON, VERT_OFF = ' O^ ━-┃|'
    EMPTY, START, END, INTERSECT, HORIZ_ON, HORIZ_OFF, VERT_ON, VERT_OFF = ' O^ ━ ┃ '

WINDOW_DESC = "The Witness"

RIGHT: Point = (1, 0)
UP: Point = (0, -1)
LEFT: Point = (-1, 0)
DOWN: Point = (0, 1)

# General color catalog
BLACK_RGB = (0, 0, 0)
CELL_BLACK_RGB = (1, 41, 31)
CELL_WHITE_RGB = (215, 218, 216)
CELL_ORANGE_RGB = (106, 180, 95)
CELL_BLUE_RGB = (102, 37, 225)
BORDER_GREEN_RGB = (7, 60, 52)
LINE_GREEN_RGB = (27, 47, 56)
INNER_CELL_GREEN_RGB = (0, 164, 130)
BACKGROUND_BROWN_RGB = (37, 21, 3)


class PuzzleConfig:
    PANEL_BOUNDING_BOX_WHISKER_START_X = (260, 380)
    PANEL_BOUNDING_BOX_WHISKER_START_Y = (180, 300)


class Region2ColorStarter(PuzzleConfig):
    '''Handles the initial starter 2-color region puzzle'''
    palette = (
        BLACK_RGB +
        CELL_BLACK_RGB +
        CELL_WHITE_RGB +
        BORDER_GREEN_RGB +
        LINE_GREEN_RGB +
        INNER_CELL_GREEN_RGB +
        BACKGROUND_BROWN_RGB
    )
    BLACK = 0
    CELL_BLACK = 1
    CELL_WHITE = 2
    BORDER_GREEN = 3
    LINE_GREEN = 4
    INNER_CELL_GREEN = 5
    BACKGROUND_BROWN = 6

    DEBUG_COLOR = CELL_WHITE

    def line_pattern(self):
        return [self.BORDER_GREEN, self.LINE_GREEN, self.LINE_GREEN, self.LINE_GREEN]

    def pixel_to_color_char(self, pixel_idx):
        if pixel_idx == self.CELL_WHITE:
            return 'w'
        elif pixel_idx == self.CELL_BLACK:
            return 'k'
        return ' '


class RegionColorTriplet(PuzzleConfig):
    '''Handles the 2 color or 3 color region puzzles'''
    palette = (
        BLACK_RGB +
        CELL_BLACK_RGB +
        CELL_WHITE_RGB +
        CELL_ORANGE_RGB +
        CELL_BLUE_RGB +
        LINE_GREEN_RGB +
        INNER_CELL_GREEN_RGB +
        BACKGROUND_BROWN_RGB
    )
    BLACK = 0
    CELL_BLACK = 1
    CELL_WHITE = 2
    CELL_ORANGE = 3
    CELL_BLUE = 4
    LINE_GREEN = 5
    INNER_CELL_GREEN = 6
    BACKGROUND_BROWN = 7

    DEBUG_COLOR = CELL_WHITE

    def line_pattern(self):
        return [self.INNER_CELL_GREEN, self.LINE_GREEN, self.LINE_GREEN, self.LINE_GREEN]

    def pixel_to_color_char(self, pixel_idx):
        if pixel_idx == self.CELL_WHITE:
            return 'w'
        elif pixel_idx == self.CELL_BLACK:
            return 'k'
        elif pixel_idx == self.CELL_BLUE:
            return 'b'
        elif pixel_idx == self.CELL_ORANGE:
            return 'o'
        return ' '


# Puzzle = Region2ColorStarter()
Puzzle = RegionColorTriplet()


