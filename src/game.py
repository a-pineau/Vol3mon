"""Implements the game loop and handles the user's events."""

import os
import random
import pygame as pg
import math

from sprites import Player, Net
from settings import *
from os.path import join, dirname, abspath
from PyQt5.QtWidgets import (QMainWindow, QApplication, QGridLayout, QWidget, QLayout)

# Manually places the window
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (100, 100)

class Game:
    def __init__(self) -> None:
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode([WIDTH, HEIGHT])
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.running = True
    
    def new(self):
        # Start a new game
        self.all_sprites = pg.sprite.Group()
        self.players = [
            Player(WIDTH / 4, HEIGHT, "GREEN"),
        ]
        self.net = Net()
        self.all_sprites.add(self.players, self. net)
    
    def run(self):
        # Game loop
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.display()
    
    def update(self):
        # Game loop update
        self.all_sprites.update()
    
    def events(self):
        # Game loop - events
        for event in pg.event.get():
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False

    def display(self):
        # Game loop - display
        self.screen.fill(BACKGROUND)
        self.all_sprites.draw(self.screen)
        pg.display.flip()

# Game loop
# def main():
#     pygame.init()
#     screen = pygame.display.set_mode([WIN_SIZE_X, WIN_SIZE_Y])
#     pygame.display.set_caption("v0lem0n")
#     net_rect = pygame.Rect(WIN_SIZE_X / 2 - NET_W / 2,  WIN_SIZE_Y - NET_H, NET_W, NET_H)
#     current_player = random.choice(players)
#     running = True
#     jumping = False

#     while running:
#         # Events handling
#         keys = pygame.key.get_pressed()
#         for event in pygame.event.get():
#             # print(pygame.mouse.get_pos())
#             # Quiting game
#             if event.type == QUIT:
#                 running = False
#             elif event.type == KEYDOWN:
#                  # Quiting (w/ escape)
#                 if event.key == K_ESCAPE:
#                     running = False
#                 elif event.key == K_SPACE:
#                     jumping = True
#         # Moving players (right/left)
#         if keys[K_RIGHT]:
#             current_player.move(1)
#         elif keys[K_LEFT]:
#             current_player.move(-1)
  
#         screen.blit(BACKGROUND_PURPLE, (0, 0))
#         pygame.draw.rect(screen, GREEN2, net_rect)
#         for p in players:
#             screen.blit(PLAYERS_ID[p.color], p.rect)
#             pygame.draw.rect(screen, RED2, p.rect, 1) # Debug
#         if jumping:
#             if current_player.rect.midbottom[1] > WIN_SIZE_Y - MAX_JUMP_H:
#                 current_player.rect.move_ip(0, -2)
#             else: 
#                 print("lol")
#                 current_player.rect.move_ip(0, 1)
#                 print(current_player.rect.midbottom)
#         pygame.display.update()
#     pygame.quit()
    
def main():
    g = Game()
    while g.running:
        g.new()
        g.run()
    
    pg.quit()

if __name__ == "__main__":
    main()