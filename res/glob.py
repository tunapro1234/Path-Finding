WIDTH = HEIGHT = 600
PIXEL_NUM = 60

TITLE = "PATH FINDING"
DRAW_GRID = False
# Animasyonların kapalı olması poerformansı uçuruyor
ANIMATIONS = 0
FPS = 500

class maps:
    blank = 0
    zebra = 1
    windows = 2
    coolerWindows = 3
    yourComputerWillCrash = 4
    
MAP = maps.yourComputerWillCrash
class colors:
    red = (255, 0, 0)
    black = (0, 0, 0)
    blue = (0, 0, 255)
    lime = (0, 255, 0)
    turq = (64, 224, 208)
    orange = (255, 69, 0)
    white = (255, 255, 255)
    green = (34, 139, 34)

class states:
    empty = 0
    start = 1
    wall = 3
    end = 4
    
    old = 5
    new = 6
    lead= 7
    final = 8
