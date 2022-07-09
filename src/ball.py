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
        self.best_angle = None

    def drop(self):
        angle = None
        xi = self.pos.x
        mag = self.vel.magnitude()
        while not angle:
            if self.pos.x < WIDTH * 0.5:
                x0 = PLAYER_RADIUS
                x1 = (WIDTH - NET_WIDTH) * 0.5 - PLAYER_RADIUS
            else:
                x0 = (WIDTH + NET_WIDTH) * 0.5 + BOT_RADIUS
                x1 = WIDTH - BOT_RADIUS
            xf = random.randint(x0, x1)
            mag = self.vel.magnitude()
            angle = self.predict_angle(xi, xf)
        # Setting new velocity
        self.vel.x = mag * cos(angle)
        self.vel.y = mag * -sin(angle)
        
    def predict_h_range(self, angle=None):
        if not angle:
            angle = radians(self.vel.angle_to(vec(1, 0)))
        # Sake of readability
        x0 = self.pos.x
        y0 = HEIGHT - self.pos.y - self.r
        v = self.vel.magnitude()
        g = BALL_GRAVITY
        # d = V₀ * cos(α) * [V₀ * sin(α) + √((V₀ * sin(α))² + 2 * g * h)] / g
        hR = v * cos(angle) 
        hR *= v * sin(angle) + sqrt((v * sin(angle))**2 + 2 * g * y0)
        hR /= g
        hR += x0
        print("range =", hR)
        return int(hR)

    def predict_x_pos(self, x0, tf):
        if tf: return x0 + self.vel.x*tf

    def predict_y_pos(self, y0, tf):
        g = BALL_GRAVITY
        if tf: return y0 - self.vel.y*tf + g*0.5*tf**2

    def predict_angle(self, x0, xf, y0=None, v=None):
        """
        TODO
        """
        if not y0: y0 = HEIGHT - self.pos.y - self.r
        if not v: v = self.vel.magnitude()
        g = BALL_GRAVITY
        # print("y0 =", y0, "x0 =", x0, "xf =", xf, "v =", v)
        try:
            c1 = (g*(xf-x0)**2/v**2 - y0) / sqrt(y0**2 + (xf-x0)**2)
            c1 = acos(c1)
        except ValueError:
            print("Impossible to reach!")
            return None
        else:
            c2 = atan(abs(xf-x0) / y0)
            angle = (c1+c2) * 0.5
            return pi - angle if xf <= x0 else angle

    def predict_time(self, yf):
        """
        TODO
        """
        y0 = self.pos.y
        g = BALL_GRAVITY
        # Solving quadratic equation
        a = -g*0.5
        b = -self.vel.y
        c = yf - y0
        delta = b**2 - 4*a*c
        try:
            sqrt(delta)
        except ValueError:
            print("The value of yf can't be reached! Returning None value.")
            return None
        else:
            t1 = (-b-sqrt(delta)) / (2*a)
            t2 = (-b+sqrt(delta)) / (2*a)
            tf = t1 if t1 >= 0 else t2
            return tf

    def predict_speed(self, tf):
        """
        TODO
        """
        vy = self.vel.y + self.acc.y * tf
        speed = sqrt(self.vel.x**2 + vy**2)
        return speed
    
    def predict_trajectory(self, h_range, angle):
        """
        TODO
        """
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

def main():
    pass

if __name__ == "__main__":
    main()




