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

PUZZLE_TYPES = (
    'Starter2Region',
    'TripletRegion',
    'Triangle',
)

Puzzle = None
def config_factory(puzzle_type):
    '''Mutating module-level global state. Yuck.'''
    global Puzzle

    print(f'Configuring for puzzle type: {puzzle_type}')
    if puzzle_type == 'Starter2Region':
        Puzzle = Region2ColorStarter()
    elif puzzle_type == 'TripletRegion':
        Puzzle = RegionColorTriplet()
    elif puzzle_type == 'Triangle':
        Puzzle = Triangle()
    else:
        raise RuntimeError(f'Unknown puzzle_type: {puzzle_type}')


RIGHT: Point = (1, 0)
UP: Point = (0, -1)
LEFT: Point = (-1, 0)
DOWN: Point = (0, 1)

# Colors of the region puzzles
BLACK_RGB = (0, 0, 0)
CELL_BLACK_RGB = (1, 41, 31)
CELL_WHITE_RGB = (215, 218, 216)
CELL_ORANGE_RGB = (106, 180, 95)
CELL_BLUE_RGB = (102, 37, 225)
BORDER_GREEN_RGB = (7, 60, 52)
LINE_GREEN_RGB = (27, 47, 56)
INNER_CELL_GREEN_RGB = (0, 164, 130)
BACKGROUND_BROWN_RGB = (37, 21, 3)

# Colors for the Triangle puzzles
TRIANGLE_BACKGROUND_RGB = (25, 20, 5)
TRIANGLE_LINE_RGB = (127, 107, 42)
TRIANGLE_ICON_RGB = (250, 187, 10)
# TRIANGLE_BROWN_RGB = (34, 17, 2)  # color of the surrounding wall

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


class Triangle(PuzzleConfig):
    '''Handles the triangle puzzle'''
    palette = (
        # BLACK_RGB +
        CELL_WHITE_RGB +
        TRIANGLE_BACKGROUND_RGB +
        TRIANGLE_LINE_RGB +
        TRIANGLE_ICON_RGB
        # TRIANGLE_BROWN_RGB
    )
    # BLACK = 0
    CELL_WHITE = 0
    TRIANGLE_BACKGROUND = 1
    TRIANGLE_LINE = 2
    TRIANGLE_ICON = 3
    # TRIANGLE_BROWN = 4

    DEBUG_COLOR = CELL_WHITE

    def line_pattern(self):
        return [self.TRIANGLE_BACKGROUND, self.TRIANGLE_LINE, self.TRIANGLE_LINE, self.TRIANGLE_LINE]
