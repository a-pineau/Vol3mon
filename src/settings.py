import os
import pygame

# Main window 
TITLE = "K@ng_-"
WIDTH = 1400
HEIGHT = 800
FPS = 60

# Directories
FILE_DIR = os.path.dirname(__file__)
IMAGES_DIR = os.path.join(FILE_DIR, "../imgs")
SNAP_FOLDER = "snapshots"

# Colours
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
BACKGROUND = (30, 30, 30)

# Net
NET_WIDTH = 20
NET_HEIGHT = 250

# Players: https://commons.wikimedia.org/wiki/File:Button_Icon_Blue.svg
PLAYER_X_SPEED = 10
PLAYER_ACC = 0.5
PLAYER_FRICTION = -0.0

SIZE_FACTOR = 0.25
PLAYER_GREEN = pygame.image.load(
    os.path.join(IMAGES_DIR, "player_green.png")
    )
PLAYER_GREEN = pygame.transform.rotozoom(PLAYER_GREEN, 0, SIZE_FACTOR)  # Adjusting size
PLAYER_BLUE = pygame.image.load(
    os.path.join(IMAGES_DIR, "player_blue.png")
    )
PLAYER_BLUE = pygame.transform.rotozoom(PLAYER_BLUE, 0, SIZE_FACTOR)  # Adjusting size

PLAYER_SIZE = PLAYER_GREEN.get_rect().size[0]
PLAYERS_ID = {
    "GREEN": PLAYER_GREEN,
    "BLUE": PLAYER_BLUE,
}

# # Balls: 
# # Ball_1: https://www.flaticon.com/fr/icone-gratuite/volley-ball_184093
# BALL_1 = pygame.image.load(
#     os.path.join(IMAGES_DIR, "ball_1.png")
#     ).convert_alpha()
# BALL_1 = pygame.transform.rotozoom(BALL_1, 0, SIZE_FACTOR) 

