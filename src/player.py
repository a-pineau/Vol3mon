"""
Sprites classes
"""

import math
import pygame as pg
import random
import numpy as np

from math import (cos, degrees, sin, tan, acos, 
                  atan, atan2, pi, radians, sqrt)
from itertools import cycle
from settings import *
vec = pg.math.Vector2

class Player(pg.sprite.Sprite):
    # -----------
    def __init__(self, game, r, x, y, vel, acc, color):
        """
        Constructor
        """
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.r = r
        self.pos = vec(x, y)
        self.vel = vel
        self.acc = acc
        self.color = color
        self.m = 3 # TODO
        self.rect = pg.Rect(self.pos.x-r, self.pos.y-r, self.r*2, self.r*2)
        self.old_rect = self.rect.copy()
        self.obstacles = self.game.obstacles

    # Should be static or in another file
    def circles_overlap(self, other) -> bool:
        """
        Checks if two circles are overlapping.

        Parameters
        ----------
        """
        return self.pos.distance_to(other.pos) < self.r + other.r

    def is_standing(self, tolerance=1, floor=True, obstacles=None) -> bool:
        standing = False
        self.rect.bottom += tolerance
        # If the ball is standing on floor
        if floor:
            standing = self.rect.bottom + tolerance > HEIGHT
        # Or on an obstacle
        if obstacles:
            if not isinstance(obstacles, pg.sprite.Group):
                obstacles_group = pg.sprite.Group()
                for obs in obstacles:
                    obstacles_group.add(obs)
            else:
                obstacles_group = obstacles
            collisions_sprite = pg.sprite.spritecollide(self, obstacles_group, False)
            if collisions_sprite:
                for sprite in collisions_sprite:
                    if (self.rect.bottom >= sprite.rect.top and 
                        self.old_rect.bottom - 1 <= sprite.old_rect.top):
                            standing = True
        self.rect.bottom -= tolerance
        return standing

    @staticmethod
    def distance(p1, p2):
        """Returns the distance between two points p1, p2."""
        return math.sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)

    @staticmethod
    def is_in_player_zone(x) -> bool:
        return x <= (WIDTH - NET_WIDTH) * 0.5 and x > 0

    @staticmethod
    def is_in_bot_zone(x) -> bool:
        return x >= (WIDTH + NET_WIDTH) * 0.5 
       
    def jump(self) -> None:  
        # Can only jump on platforms or floor
        if self.is_standing(PLAYER_JUMP_TOLERANCE, True, self.game.obstacles): 
            self.vel.y = -PLAYER_Y_SPEED
        
    def screen_collisions(self, orientation, is_ball) -> None:
        """
        Deals with screen collisions (left/right/top/bottom borders)

        Parameters
        ----------

        """
        old_vel = (int(self.vel.x), int(self.vel.y))
        if orientation == "horizontal":
            # Right border
            if self.rect.right > WIDTH:
                self.game.stop_timer = True
                self.rect.right = WIDTH
                self.pos.x = self.rect.centerx
                if is_ball: self.vel.x *= -1
            # Left border
            elif self.rect.left < 0:
                self.rect.left = 0
                self.pos.x = self.rect.centerx
                if is_ball: self.vel.x *= -1
        if orientation == "vertical":
            # Bottom border
            if self.rect.bottom >= HEIGHT:
                self.rect.bottom = HEIGHT
                self.pos.y = self.rect.centery
                if is_ball:
                    print("landing vel =", self.vel.magnitude())
                    print("landing =", self.rect.centerx)
                    self.vel.y *= -1 
                else: 
                    self.vel.y *= 0
            # Top border
            elif self.rect.top < 0:
                self.rect.top = 0
                self.pos.y = self.rect.centery
                self.vel.y *= -1
        # Checking if a collision happened
        if is_ball and old_vel != (int(self.vel.x), int(self.vel.y)):
            self.predict_trajectory()
            self.game.bot.predict_move()

    def obstacles_collisions(self, orientation, is_ball):
        """
        Deals with side collisions with obstacles.

        Parameters
        ----------

        """
        collisions_sprites = pg.sprite.spritecollide(self, self.obstacles, False)
        if collisions_sprites:
            for sprite in collisions_sprites:
                if orientation == "horizontal":
                    # Right side collision
                    if (self.rect.right >= sprite.rect.left and 
                        self.old_rect.right - 1 <= sprite.old_rect.left):
                            self.rect.right = sprite.rect.left
                            self.pos.x = self.rect.centerx
                            if is_ball: self.vel.x *= -1
                    # Left side collision
                    if (self.rect.left <= sprite.rect.right and 
                        self.old_rect.left + 1 >= sprite.old_rect.right):
                            self.rect.left = sprite.rect.right
                            self.pos.x = self.rect.centerx
                            if is_ball: self.vel.x *= -1
            for sprite in collisions_sprites:
                if orientation == "vertical":
                    # Top side collision
                    if (self.rect.bottom >= sprite.rect.top and 
                        self.old_rect.bottom - 1 <= sprite.old_rect.top):
                            self.rect.bottom = sprite.rect.top
                            self.pos.y = self.rect.centery
                            self.vel.y *= -1 if is_ball else 0
                    # Bottom side collision
                    if (self.rect.top <= sprite.rect.bottom and 
                        self.old_rect.top + 1 >= sprite.old_rect.bottom):
                            self.rect.top = sprite.rect.bottom
                            self.pos.y = self.rect.centery
                            self.vel.y *= -1
            if is_ball:
                # Predicting bot's move
                self.predict_trajectory()
                self.game.bot.predict_move()

    def on_air_ball_collision(self, other):
        """
        TODO

        Parameters
        ----------
        """
        balls_in_the_air = not self.is_standing() and not other.is_standing()
        if self.circles_overlap(other) and balls_in_the_air: 
            x1, x2 = self.pos, other.pos
            m1, m2 = self.r**2, other.r**2
            M = m1 + m2
            R = self.r + other.r
            v1, v2 = self.vel, other.vel
            # The distance has already been computed, can simplify here
            d = pg.math.Vector2.magnitude(x1 - x2)
            disp = (d - R) * 0.5
            n = vec(x2[0]-x1[0], x2[1]-x1[1])  
            # Computing new velocities
            n_v1 = v1 - 2*m2 / M * vec.dot(v1-v2, x1-x2) * (x1-x2) / d**2
            n_v2 = v2 - 2*m1 / M * vec.dot(v2-v1, x2-x1) * (x2-x1) / d**2
            self.vel = n_v1
            other.vel = n_v2
            # Dealing with sticky collisions issues
            self.pos.x += disp * (n.x / d)
            self.pos.y += disp * (n.y / d)
            other.pos.x -= disp * (n.x / d) 
            other.pos.y -= disp * (n.y / d)
            # Predicting bot's move
            self.game.bot.predict_move()

    def on_floor_ball_collision(self):
        """
        TODO

        Parameters
        ----------
        """
        # Sake of readability
        ball = self.game.ball 
        bot = self.game.bot
        if self.circles_overlap(ball):
            print("pos bally=", ball.pos.y)
            dx = ball.pos.x - self.pos.x
            dy = ball.pos.y - self.pos.y
            R = self.r + ball.r
            d = pg.math.Vector2.magnitude(ball.pos - self.pos)
            disp = (d - R) * 0.5
            n = vec(dx, dy)
            angle = abs(atan2(dy, dx))
            # Computing new velocities
            mag = ball.vel.magnitude()
            ball.vel.x = mag*cos(angle)
            ball.vel.y = mag*-sin(angle)
            # Dealing with sticky collisions
            ball.pos.x -= disp*(n.x / d)
            ball.pos.y -= disp*(n.y / d)
            # Predicting bot move 
            # ball.predict_trajectory()
            # bot.predict_move()

    def end_round_conditions(self) -> bool:
        """
        TODO

        Parameters
        ----------
        """
        # If the ball hits the floor and is in the player/bot zone
        if self == self.game.ball:
            if self.is_standing():
                if self.is_in_bot_zone(self.rect.left):
                    self.game.scores["Player"] += 1
                elif self.is_in_player_zone(self.rect.right):
                    self.game.scores["Bot"] += 1
                return True
        # If player/bot goes into its wrong zone
        else:
            if self == self.game.bot and self.is_in_player_zone(self.rect.right):
                self.game.scores["Player"] += 1
                return True
            elif self == self.game.player and self.is_in_bot_zone(self.rect.left):
                self.game.scores["Bot"] += 1
                return True
        return False

    def update(self):
        """
        Updates positions and applies collisions (if any).

        Parameters
        ----------
        """
        is_ball = (self == self.game.ball)
        # Rect at previous frame
        self.old_rect = self.rect.copy()
        if self == self.game.player: # Player only
            self.vel.x = 0
            keys = pg.key.get_pressed() # Keyboard events
            if keys[pg.K_RIGHT]:
                self.vel.x += PLAYER_X_SPEED
            elif keys[pg.K_LEFT]:
                self.vel.x += -PLAYER_X_SPEED
        # Updating velocity (no change in the horizontal component)
        self.vel.y += self.acc.y
        # Updating x pos
        self.pos.x += self.vel.x
        self.rect.centerx = self.pos.x
        # # Screen collisions (horitonzal)
        self.screen_collisions("horizontal", is_ball)
        # Obstacles collisions (horizontal)
        self.obstacles_collisions("horizontal", is_ball)
        # Updating y pos
        self.pos.y += self.vel.y + 0.5*self.acc.y
        self.rect.centery = self.pos.y
        # Screen collisions (vertical)
        self.screen_collisions("vertical", is_ball)
        # Obstacles collisions (vertical)
        self.obstacles_collisions("vertical", is_ball)       
        # Ball collision (on floor)
        if not is_ball and self.is_standing():
            self.on_floor_ball_collision()
        else:
            particles = self.game.balls.sprites()
            for i, p in enumerate(particles):
                for other in particles[i+1:]:
                    p.on_air_ball_collision(other)


def main():
    pass

if __name__ == "__main__":
    main()




