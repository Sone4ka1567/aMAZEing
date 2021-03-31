from tkinter import Tk


root = Tk()

# colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
LIGHTGREY = (100, 100, 100)
SKYBLUE = (135, 206, 235)
ORCHID = (218, 112, 214)
DARKBLUE = (0, 153, 153)

# game settings
WIDTH = root.winfo_screenwidth()
HEIGHT = root.winfo_screenheight() - 100
FPS = 60
TITLE = "aMAZEing"
BACKGROUND_COLOR = SKYBLUE
CELL_SIZE = 32
GRID_WIDTH = WIDTH / CELL_SIZE
GRID_HEIGHT = HEIGHT / CELL_SIZE

PLAYER_SPEED = 4
