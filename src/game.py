"""Implements the game loop and handles the user's events."""

import os
import random
import pygame as pg
import math

from sprites import Player, BallGame, Platform
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
        # Defining sprite groups
        self.balls = pg.sprite.Group()
        self.players = pg.sprite.Group()
        self.platforms = pg.sprite.Group()
        self.all_sprites = pg.sprite.Group()

        # Defining balls
        self.player = Player(self, WIDTH / 4, HEIGHT, "BALL_PLAYER_1") # Player 1
        self.ball_game = BallGame(self, WIDTH / 4, HEIGHT / 2, "BALL_GAME", (0, 0)) # Ball game
        # Defining platforms
        self.p_net = Platform(
            WIDTH / 2, HEIGHT - NET_HEIGHT / 2,
            NET_WIDTH, NET_HEIGHT, GREEN, 0, 0)
        self.p_moving = Platform( 
            WIDTH / 2, 200, NET_WIDTH, 150, BLUE, 0, 0.75, self)
        # Adding to sprite groups
        # self.balls.add(self.ball_game)
        self.players.add(self.player)
        self.platforms.add(self.p_net)
        self.all_sprites.add(
            self.p_net,
            self.player,
        )
    
    def run(self):
        # Game loop
        self.playing = True
        self.round_over = False
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
        # print(pg.mouse.get_pos())
        for event in pg.event.get():
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                self.player.jump()
                    
    def display(self):
        # Game loop - display
        self.screen.fill(BACKGROUND)
        self.all_sprites.draw(self.screen)
        pg.display.flip()


def main():
    g = Game()
    while g.running:
        g.new()
        g.run()
    
    pg.quit()

if __name__ == "__main__":
    main()