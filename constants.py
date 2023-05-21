WIDTH, HEIGHT = 600,600
ROWS,COLS = 8,8
SQUARE_SIZE = WIDTH//COLS


#Colors
BLACK = (0,0,0)
WHITE = (255,255,255)
GREEN = (45,162,39)
LIGHT_GREEN = (152,251,152)
BROWN = (150,75,0)
LIGHT_BROWN = (181,101,29)
BEIGE = (225,225,220)
BLUE = (0,0,255)


# Find piece from mouse
def get_row_col_mouse(pos):
    x,y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row,col
