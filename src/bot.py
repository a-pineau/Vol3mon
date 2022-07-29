"""
Sprites classes
"""

import math
import pygame as pg
import random
import numpy as np

from player import Player
from math import (cos, degrees, sin, tan, acos, 
                  atan, atan2, pi, radians, sqrt)
from itertools import cycle
from settings import *
vec = pg.math.Vector2

class Bot(Player):
    def __init__(self, game, r, x, y, vel, acc, color):
        super().__init__(game, r, x, y, vel, acc, color)
        self.ball_x = None
        self.direction = 0
        self.spot = None
        self.ball = self.game.ball

    def predict_move(self):
        """
        TODO

        Parameters
        ----------
        """
        tf = self.ball.predict_time(HEIGHT - 2*self.r - self.ball.r)
        ball_spot = self.ball.predict_x(tf) 
        if ball_spot and self.is_in_bot_zone(ball_spot):
            self.spot = ball_spot + self.ball.r + self.r*0.25
            self.direction = 1 if self.spot > self.pos.x else -1

    def update(self):
        """
        TODO

        Parameters
        ----------
        """
        self.vel.x = 0
        if self.spot:
            if self.pos.x < self.spot and self.direction == -1:
                self.direction = 0
            if self.pos.x > self.spot and self.direction == 1:
                self.direction = 0
            self.vel.x += self.direction * BOT_X_SPEED
            # Updating velocity
            self.vel += self.acc
            # Updating x pos
            self.pos.x += self.vel.x + 0.5 * self.acc.x
            self.rect.centerx = self.pos.x
            # Screen collisions (horitonzal)
            self.screen_collisions("horizontal", False)
            # Obstacles collisions (horizontal)
            self.obstacles_collisions("horizontal", False)
            # Updating y pos
            self.pos.y += self.vel.y + 0.5 * self.acc.y
            self.rect.centery = self.pos.y
            # Screen collisions (vertical)
            self.screen_collisions("vertical", False)
            # Obstacles collisions (vertical)
            self.obstacles_collisions("vertical", False) 
            # Ball collision (on floor)
        if self.is_standing():
            self.on_floor_ball_collision()

    def drunk_mode(self):
        pass

    def normal_mode(self):
        pass

    def skilled_mode(self):
        pass


def main():
    pass

if __name__ == "__main__":
    main()




