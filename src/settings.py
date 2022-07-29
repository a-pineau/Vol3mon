import os
import pygame as pg

vec = pg.math.Vector2

# Main window 
TITLE = "v0lem0n"
WIDTH = 1200
HEIGHT = 600
FPS = 60

# Directories
FILE_DIR = os.path.dirname(__file__)
IMAGES_DIR = os.path.join(FILE_DIR, "../imgs")
SNAP_FOLDER = os.path.join(FILE_DIR, "../snapshots")

# Colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
GREEN2 = (39, 151, 0)
GREEN3 = (102, 203, 112)
ORANGE = (255, 127, 0)
BACKGROUND = (30, 30, 30)

# Player
PLAYER_X_SPEED = 7
PLAYER_Y_SPEED = 14
PLAYER_GRAVITY = 0.3
PLAYER_COLOR = RED
PLAYER_JUMP_TOLERANCE = 10
PLAYER_RADIUS = 50
PLAYER_INIT_X = WIDTH*0.25
PLAYER_INIT_Y = HEIGHT - PLAYER_RADIUS
PLAYER_INIT_VEL = vec(0, 0)
PLAYER_INIT_ACC = vec(0, PLAYER_GRAVITY)
PLAYER_SETTINGS = [
    PLAYER_RADIUS,
    PLAYER_INIT_X,
    PLAYER_INIT_Y,
    PLAYER_INIT_VEL,
    PLAYER_INIT_ACC,
    PLAYER_COLOR,
]

# Bot
BOT_X_SPEED = PLAYER_X_SPEED
BOT_RADIUS = PLAYER_RADIUS
BOT_INIT_X = WIDTH*0.75
BOT_INIT_Y = HEIGHT - BOT_RADIUS
BOT_INIT_VEL = vec(0, 0)
BOT_INIT_ACC = vec(0, PLAYER_GRAVITY)
BOT_COLOR = BLUE
BOT_SETTINGS = [
    BOT_RADIUS,
    BOT_INIT_X,
    BOT_INIT_Y,
    BOT_INIT_VEL,
    BOT_INIT_ACC,
    BOT_COLOR,
]

# Ball game
BALL_GRAVITY = 0.3
BALL_RADIUS = 45
BALL_INIT_X = BOT_INIT_X # Human player always starts
BALL_INIT_Y = HEIGHT*0.2 # Arbitrary
BALL_INIT_VEL_X = -2
BALL_INIT_VEL_Y = 0
BALL_INIT_VEL = vec(BALL_INIT_VEL_X, BALL_INIT_VEL_Y)
BALL_INIT_ACC = vec(0, BALL_GRAVITY)
BALL_COLOR = YELLOW
BALL_SETTINGS = [
    BALL_RADIUS,
    BALL_INIT_X,
    BALL_INIT_Y,
    BALL_INIT_VEL,
    BALL_INIT_ACC,
    BALL_COLOR,
]

# Net
NET_HEIGHT = 200
NET_POS_X = WIDTH * 0.5
NET_POS_Y = HEIGHT - NET_HEIGHT * 0.5
NET_WIDTH = 20
NET_COLOR = WHITE
NET_VEL = vec(0, 0)
NET_SETTINGS = [
    NET_POS_X,
    NET_POS_Y,
    NET_WIDTH,
    NET_HEIGHT,
    NET_COLOR,
    NET_VEL,
]

# Moving platform
MOVING_PLATFORM_HEIGHT = 120
MOVING_PLATFORM_POS_X = WIDTH * 0.5
MOVING_PLATFORM_POS_Y = HEIGHT * 0.3
MOVING_PLATFORM_WIDTH = 10
MOVING_PLATFORM_COLOR = GREEN
MOVING_PLATFORM_VEL = vec(0, -2)
MOVING_PLATFORM_SETTINGS = [
    MOVING_PLATFORM_POS_X,
    MOVING_PLATFORM_POS_Y,
    MOVING_PLATFORM_WIDTH,
    MOVING_PLATFORM_HEIGHT,
    MOVING_PLATFORM_COLOR,
    MOVING_PLATFORM_VEL,
]

# MESSAGES
# Start round
START_ROUND_MSG = "Hit the spacebar to start"
START_ROUND_FONT_SIZE = 35
START_ROUND_COLOR = WHITE
START_ROUND_POSITION = WIDTH * 0.5, HEIGHT * 0.5
START_ROUND_SETTINGS = [
    START_ROUND_MSG,
    START_ROUND_FONT_SIZE,
    START_ROUND_COLOR,
    START_ROUND_POSITION
]




