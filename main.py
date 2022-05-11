"""Implements the game loop and handles the user's events."""

import sys
import os
import random

from os.path import join, dirname, abspath
# Manually places the window
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (100, 100)
sys.path.insert(0, abspath(join(dirname(__file__), "src")))

import math
import pygame
from player import Player
from display_features import *
from constants import *
from PyQt5.QtWidgets import (QMainWindow, QApplication, QGridLayout, QWidget, QLayout)
SNAP_FOLDER = os.path.join(os.path.dirname(__file__), "results")
n_snap = 0
players = [
    # Player(1 * WIN_SIZE_X / 4, WIN_SIZE_Y + LOD, "GREEN"), 
    Player(3 * WIN_SIZE_X / 4, WIN_SIZE_Y + LOD, "BLUE"), 
]


# Game loop
def main():
    pygame.init()
    screen = pygame.display.set_mode([WIN_SIZE_X, WIN_SIZE_Y])
    pygame.display.set_caption("v0lem0n")
    net_rect = pygame.Rect(WIN_SIZE_X / 2 - NET_W / 2,  WIN_SIZE_Y - NET_H, NET_W, NET_H)
    current_player = random.choice(players)
    running = True
    jumping = False

    while running:
        # Events handling
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            # print(pygame.mouse.get_pos())
            # Quiting game
            if event.type == QUIT:
                running = False
            elif event.type == KEYDOWN:
                 # Quiting (w/ escape)
                if event.key == K_ESCAPE:
                    running = False
                elif event.key == K_SPACE:
                    jumping = True
        # Moving players (right/left)
        if keys[K_RIGHT]:
            current_player.move(1)
        elif keys[K_LEFT]:
            current_player.move(-1)
  
        screen.blit(BACKGROUND_PURPLE, (0, 0))
        pygame.draw.rect(screen, GREEN2, net_rect)
        for p in players:
            screen.blit(PLAYERS_ID[p.color], p.rect)
            pygame.draw.rect(screen, RED2, p.rect, 1) # Debug
        if jumping:
            if current_player.rect.midbottom[1] > WIN_SIZE_Y - MAX_JUMP_H:
                current_player.rect.move_ip(0, -2)
            else: 
                print("lol")
                current_player.rect.move_ip(0, 1)
                print(current_player.rect.midbottom)
        pygame.display.update()
    pygame.quit()
    

if __name__ == "__main__":
    main()