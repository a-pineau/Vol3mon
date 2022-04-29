import os
import pygame

# Main window 
TITLE = "K@ng_-"
WIDTH = 1600
HEIGHT = 900
FPS = 144

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
ORANGE = (255, 127, 0)
BACKGROUND = (30, 30, 30)

# Net
NET_WIDTH = 20
NET_HEIGHT = 250

# Players:
PLAYER_X_SPEED = 6
PLAYER_Y_SPEED = -25
PLAYER_ACC = 0.5
PLAYER_FRICTION = -0.02
PLAYER_GRAVITY = 0.75

# Ball game:
BALL_GRAVITY = 0.05

# MISC
COLLISION_TOLERANCE = 10

# Images (https://icons-for-free.com/ball-1319987875440295270/)
BALL_PLAYER_1 = pygame.image.load(
    os.path.join(IMAGES_DIR, "ball_player_1.png")
    )
BALL_PLAYER_1 = pygame.transform.rotozoom(BALL_PLAYER_1, 0, 0.9)  # Adjusting size
BALL_GAME = pygame.image.load(
    os.path.join(IMAGES_DIR, "ball_game.png")
    )
BALL_GAME = pygame.transform.rotozoom(BALL_GAME, 0, 0.2)  # Adjusting size
PLAYERS_ID = {
    "BALL_PLAYER_1": BALL_PLAYER_1,
    "BALL_GAME": BALL_GAME,
}

# # Balls: 
# # Ball_1: https://www.flaticon.com/fr/icone-gratuite/volley-ball_184093
# BALL_1 = pygame.image.load(
#     os.path.join(IMAGES_DIR, "ball_1.png")
#     ).convert_alpha()
# BALL_1 = pygame.transform.rotozoom(BALL_1, 0, SIZE_FACTOR) 

