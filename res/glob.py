WIDTH = HEIGHT = 400
PIXEL_NUM = 20

TITLE = "PATH FINDING"
DRAW_GRID = False
FPS = 500
MAP = 3

class colors:
    red = (255, 0, 0)
    blue = (0, 0, 255)
    green = (0, 255, 0)
    white = (255, 255, 255)
    black = (0, 0, 0)
    turq = (64, 224, 208)
    orange = (255, 69, 0)

class states:
    empty = 0
    start = 1
    wall = 3
    end = 4
    
    old = 5
    new = 6
    final = 7