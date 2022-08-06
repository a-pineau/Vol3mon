"""
Sprites classes
"""

import math
import pygame as pg
import random
import numpy as np

from player import Player
from math import cos, sin, acos, atan, pi, radians, sqrt
from itertools import cycle
from settings import *
vec = pg.math.Vector2

class Ball(Player):
    def __init__(self, game, r, x, y, vel, acc, color):
        super().__init__(game, r, x, y, vel, acc, color)
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

    def predict_trajectory(self, inc=0.5):
        """
        TODO

        Parameters
        ----------

        """
        yf = HEIGHT - self.r
        tf = self.predict_time(yf)
        # We're creating a fake ball thats not gonna be displayed
        fake_ball = Ball(
            self.game, 
            BALL_RADIUS,
            self.pos.x,
            self.pos.y,
            vec(self.vel.x, self.vel.y),
            vec(0, BALL_GRAVITY),
            BALL_COLOR
        )
        obstacles = pg.sprite.Group()
        obstacles.add(self.game.left, self.game.right, self.game.top, self.game.net)
        t = 0
        while t < tf:
            x, y = self.predict_x(t), self.predict_y(t)
            fake_ball.pos.x, fake_ball.pos.y = x, y
            fake_ball.rect.center = (x, y)
            collision = pg.sprite.spritecollide(fake_ball, obstacles, False)
            if collision:
                fake_ball.vel = vec(-self.vel.x, fake_ball.predict_vy(self.vel.y, t))
                return fake_ball.predict_range()
            t += inc
        return x
        
    def predict_range(self):
        """
        Predicts horizontal range.
        Eq: hR = V₀ * cos(α) * [V₀ * sin(α) + √((V₀ * sin(α))² + 2 * g * h)] / g

        Parameters
        ----------

        Returns
        -------
        """
        angle = radians(self.vel.angle_to(vec(1, 0)))
        x0 = self.pos.x
        y0 = HEIGHT - self.pos.y - self.r
        v = self.vel.magnitude()
        g = BALL_GRAVITY
        r = v*cos(angle) 
        r *= v*sin(angle) + sqrt((v*sin(angle))**2 + 2*g*y0)
        r /= g
        r += x0
        return int(r)

    def predict_x(self, t):
        """
        TODO

        Parameters
        ----------

        Returns
        -------
        """
        if t is not None:
            x0 = self.pos.x
            return x0 + self.vel.x*t

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

    # Not used (yet?)
    def predict_angle(self, x0, xf):
        """
        TODO

        Parameters
        ----------

        Returns
        -------
        """
        y0 = HEIGHT - self.pos.y - self.r
        v = self.vel.magnitude()
        g = BALL_GRAVITY
        try:
            c1 = (g*(xf-x0)**2/v**2 - y0) / sqrt(y0**2 + (xf-x0)**2)
            c1 = acos(c1)
        except ValueError:
            print("Impossible to reach!")
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

    def predict_vy(self, vy_init, t):
        """
        Predicts speed.

        Parameters
        ----------

        Returns
        -------
        """
        vy = vy_init + self.acc.y*t
        return vy
                
def main():
    pass

if __name__ == "__main__":
    main()




