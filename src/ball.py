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

class Ball(Player):
    def __init__(self, game, r, x, y, vel, acc, color):
        super().__init__(game, r, x, y, vel, acc, color)
        self.trajectory = []
        self.drop()

    def drop(self):
        angle = None
        while not angle:
            if self.pos.x < WIDTH * 0.5:
                x0 = PLAYER_RADIUS
                x1 = (WIDTH - NET_WIDTH) * 0.5 - PLAYER_RADIUS
            else:
                x0 = (WIDTH + NET_WIDTH) * 0.5 + BOT_RADIUS
                x1 = WIDTH - BOT_RADIUS
            xf = random.randint(x0, x1)
            mag = self.vel.magnitude()
            angle = self.predict_angle(
                self.pos.x,
                xf,
                HEIGHT - self.pos.y - self.r,
                BALL_GRAVITY,
                mag)
        self.vel.x = mag * cos(angle)
        self.vel.y = mag * -sin(angle)
        print('MDR')
        self.predict_h_range(angle)

    def predict_h_range(self, angle):
        # Sake of readability
        x0 = int(self.pos.x)
        y0 = HEIGHT - self.pos.y - self.r
        v = self.vel.magnitude()
        g = BALL_GRAVITY
        # d = V₀ * cos(α) * [V₀ * sin(α) + √((V₀ * sin(α))² + 2 * g * h)] / g
        h_R = v * cos(angle) 
        h_R *= v * sin(angle) + sqrt((v * sin(angle))**2 + 2 * g * y0)
        h_R /= g
        h_R -= x0
        print("h_range =", h_R)
        return int(h_R)

    def predict_trajectory(self, h_range, angle):
        self.trajectory.clear()
        x0 = int(self.pos.x)
        y0 = self.pos.y
        v = self.vel.magnitude()
        g = BALL_GRAVITY
        buffer_rect = pg.Rect(
            self.pos.x - self.r, self.pos.y - self.r, 
            self.r*2, self.r*2)
        if x0 < h_range + 1:
            x_values = range(x0, h_range + 1, 1)
        else:
            x_values = range(x0, h_range + 1, -1)
        # y = h - [(x - x0) * tan(α) - g * (x - x0)² / (2 * V₀² * cos²(α))]
        """Note: this isn't exactly the commonly used equation as the numerical value of
        the y component of the ball position firslty decreases, after collision (due to Pygame's frame). 
        Also, the shift needs to be taken into consideration (x - x0).
        """
        for x in x_values:
            y = y0 - (x - x0) * tan(angle) + g * (x - x0)**2 / (2*v**2 * cos(angle)**2)
            buffer_rect.center = (x, y)
            self.trajectory.append((x, y))
            if buffer_rect.colliderect(self.game.net):
                self.game.bot.ball_landing_point = (WIDTH + NET_WIDTH) * 0.5
                return None
        for v in self.trajectory:
            # print(v)
            pass

    def compute_y_pos(self, yf, angle):
        """
        TODO
        """
        x0 = self.pos.x
        y0 = self.pos.y
        v = self.vel.magnitude()
        g = BALL_GRAVITY    
        c1 = 2*v**2 * cos(angle)**2
        c2 = g*x0**2 + c1*(y0+x0*tan(angle)-yf)
        a = g
        b = -2*g*x0 - c1*tan(angle)
        c = c2
        delta = b**2 - 4*a*c
        print("delta =", delta)
        x1 = (-b-sqrt(delta)) / 2*a
        x2 = (-b+sqrt(delta)) / 2*a
        print("x1, x2 =", x1, x2)
        pass

    def compute_y_pos2(self, yf, angle):
        x0 = self.pos.x
        y0 = self.pos.y
        g = BALL_GRAVITY
        v = self.vel.magnitude()
        a = g / (2*v**2*cos(angle)**2)
        b = -tan(angle)
        c = y0 - yf
        delta = b**2 - 4*a*c
        print("delta =", delta)
        X1 = (-b - sqrt(delta)) / 2*a
        X2 = (-b + sqrt(delta)) / 2*a
        x1, x2 = X1 + x0, X2 + x0
        print("x1, x2 =", x1, x2)

    def predict_angle(self, x0, xf, h, g, v):
        """
        TODO
        """
        g = BALL_GRAVITY
        try:
            c1 = (g*(xf-x0)**2/v**2 - h) / sqrt(h**2 + (xf-x0)**2)
            c1 = acos(c1)
        except ValueError:
            # print("Impossible to reach!")
            return None
        else:
            c2 = atan(abs(xf-x0)/h)
            angle = (c1 + c2) * 0.5
            return pi - angle if xf <= x0 else angle


def main():
    pass

if __name__ == "__main__":
    main()




