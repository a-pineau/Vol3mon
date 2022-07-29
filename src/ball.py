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
        """
        TODO
        """
        angle = None
        xi = self.pos.x
        while not angle:
            if self.pos.x < WIDTH*0.5:
                x0 = PLAYER_RADIUS
                x1 = (WIDTH - NET_WIDTH)*0.5 - PLAYER_RADIUS
            else:
                x0 = (WIDTH + NET_WIDTH)*0.5 + BOT_RADIUS
                x1 = WIDTH - BOT_RADIUS
            xf = random.randint(x0, x1)
            angle = self.predict_angle(xi, xf)
        # Setting new velocity
        v = self.vel.magnitude()
        self.vel.x = v * cos(angle)
        self.vel.y = v * -sin(angle)
        
    def predict_h_range(self, angle=None):
        """
        Predicts horizontal range.
        Eq: hR = V₀ * cos(α) * [V₀ * sin(α) + √((V₀ * sin(α))² + 2 * g * h)] / g

        Parameters
        ----------

        Returns
        -------
        """
        if not angle:
            angle = radians(self.vel.angle_to(vec(1, 0)))
        x0 = self.pos.x
        y0 = HEIGHT - self.pos.y - self.r
        v = self.vel.magnitude()
        g = BALL_GRAVITY
        r = v * cos(angle) 
        r *= v * sin(angle) + sqrt((v * sin(angle))**2 + 2 * g * y0)
        r /= g
        r += x0
        print("range =", r)
        return int(r)

    def predict_x(self, tf):
        """
        TODO

        Parameters
        ----------

        Returns
        -------
        """
        if tf: 
            x0 = self.pos.x
            return x0 + self.vel.x*tf

    def predict_y(self, t):
        """
        TODO

        Parameters
        ----------

        Returns
        -------
        """
        if t is not None:
            y0 = self.pos.y
            g = BALL_GRAVITY
            return y0 + self.vel.y*t + g*0.5*t**2

    def predict_angle(self, x0, xf, y0=None, v=None):
        """
        TODO

        Parameters
        ----------

        Returns
        -------
        """
        if not y0: 
            y0 = HEIGHT - self.pos.y - self.r
        if not v: 
            v = self.vel.magnitude()
        g = BALL_GRAVITY
        # print("y0 =", y0, "x0 =", x0, "xf =", xf, "g =", g, "v =", v)
        try:
            c1 = (g*(xf-x0)**2/v**2 - y0) / sqrt(y0**2 + (xf-x0)**2)
            c1 = acos(c1)
        except ValueError:
            # print("Impossible to reach!")
            return None
        else:
            c2 = atan(abs(xf-x0) / y0)
            angle = (c1+c2) * 0.5
            if xf <= x0:
                return pi - angle
            return angle

    def predict_time(self, yf):
        """
        TODO

        Parameters
        ----------

        Returns
        -------
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
            # print("The value of yf can't be reached! Returning None value.")
            return None
        else:
            t1 = (-b-sqrt(delta)) / (2*a)
            t2 = (-b+sqrt(delta)) / (2*a)
            if t1 >= 0:
                return t1
            return t2

    def predict_speed(self, t):
        """
        Predicts speed.

        Parameters
        ----------

        Returns
        -------
        """
        vy = self.vel.y + self.acc.y*t
        speed = sqrt(self.vel.x**2 + vy**2)
        return speed
                
    def predict_trajectory(self, inc=0.5):
        """
        TODO

        Parameters
        ----------

        """
        self.trajectory.clear()
        y = self.pos.y
        yf = HEIGHT - self.r
        tf = self.predict_time(yf)
        t = 0
        while t < tf:
            t += inc
            x = self.predict_x(t)
            y = self.predict_y(t)
            self.trajectory.append((x, y))

    # def predict_trajectory(self, bot_collision=False, num_inc=100):
    #     """
    #     TODO

    #     Parameters
    #     ----------

    #     """
    #     self.trajectory.clear()
    #     xf = self.predict_h_range()
    #     angle = radians(self.vel.angle_to(vec(1, 0)))
    #     x0, y0 = self.pos.x, self.pos.y
    #     v = self.vel.magnitude()
    #     g = BALL_GRAVITY
    #     rect = pg.Rect(
    #         self.pos.x - self.r, self.pos.y - self.r, 
    #         self.r*2, self.r*2)
    #     if x0 < xf :
    #         x_values = np.linspace(x0, xf, num_inc)
    #     else:
    #         x_values = np.linspace(xf, x0, num_inc)
    #     # y = h - [(x - x0) * tan(α) - g * (x - x0)² / (2 * V₀² * cos²(α))]
    #     """Note: this isn't exactly the commonly used equation as the numerical value of
    #     the y component of the ball position firslty decreases, after collision (due to Pygame's frame). 
    #     Also, the shift needs to be taken into consideration (x - x0).
    #     """
    #     for x in x_values:
    #         y = y0 - (x - x0)*tan(angle) + g*(x - x0)**2 / (2*v**2 * cos(angle)**2)
    #         rect.center = (x, y)
    #         self.trajectory.append((x, y))
    #         # Checks for any collision with an obstacle
    #         if rect.colliderect(self.game.net):
    #             self.game.bot.ball_landing_point = (WIDTH + NET_WIDTH)*0.5
    #             return None

def main():
    pass

if __name__ == "__main__":
    main()




