"""
Sprites classes
"""

import math
import pygame as pg
import numpy as np

from math import cos, sin, sqrt
from itertools import cycle
from settings import *
vec = pg.math.Vector2


# BALL -------------------------------------------------------
class Ball(pg.sprite.Sprite):
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
        self.rect = pg.Rect(self.pos.x - r, self.pos.y - r, self.r*2, self.r*2)
        self.old_rect = self.rect.copy()
        self.obstacles = self.game.obstacles

    # Should be static or in another file
    def circle_2_circle_overlap(self, other) -> bool:
        """
        Checks if two circles are overlapping
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
    def is_in_player_zone(x) -> bool:
        return x <= (WIDTH - NET_WIDTH) * 0.5

    @staticmethod
    def is_in_bot_zone(x) -> bool:
        return x >= (WIDTH + NET_WIDTH) * 0.5 
       
    def jump(self) -> None:  
        # Can only jump on platforms or floor
        if self.is_standing(PLAYER_JUMP_TOLERANCE, True, self.game.obstacles): 
            self.vel.y = -PLAYER_Y_SPEED
        
    def screen_collisions(self, orientation, is_gameball) -> None:
        """
        Deals with screen collisions (left/right/top/bottom borders)
        """
        old_vel = (int(self.vel.x), int(self.vel.y))
        if orientation == "horizontal":
            # Right border
            if self.rect.right > WIDTH:
                self.rect.right = WIDTH
                self.pos.x = self.rect.centerx
                if is_gameball:
                    self.vel.x *= -1
            # Left border
            elif self.rect.left < 0:
                self.rect.left = 0
                self.pos.x = self.rect.centerx
                if is_gameball:
                    self.vel.x *= -1
        if orientation == "vertical":
            # Bottom border
            if self.rect.bottom >= HEIGHT:
                self.rect.bottom = HEIGHT
                self.pos.y = self.rect.centery
                if is_gameball:
                    print("landing=", self.rect.centerx)
                    self.vel.y *= -1
                else:
                    self.vel.y = 0
            # Top border
            elif self.rect.top < 0:
                self.rect.top = 0
                self.pos.y = self.rect.centery
                self.vel.y *= -1
        if old_vel != (int(self.vel.x), int(self.vel.y)):
            self.game.bot.predict_move()

    def obstacles_collisions(self, orientation, is_gameball):
        """
        Deals with side collisions with obstacles
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
                            if is_gameball: self.vel.x *= -1
                    # Left side collision
                    if (self.rect.left <= sprite.rect.right and 
                        self.old_rect.left + 1 >= sprite.old_rect.right):
                            self.rect.left = sprite.rect.right
                            self.pos.x = self.rect.centerx
                            if is_gameball: self.vel.x *= -1
            for sprite in collisions_sprites:
                if orientation == "vertical":
                    # Top side collision
                    if (self.rect.bottom >= sprite.rect.top and 
                        self.old_rect.bottom - 1 <= sprite.old_rect.top):
                            self.rect.bottom = sprite.rect.top
                            self.pos.y = self.rect.centery
                            if is_gameball: 
                                self.vel.y *= -1
                            else:
                                self.vel.y = 0
                    # Bottom side collision
                    if (self.rect.top <= sprite.rect.bottom and 
                        self.old_rect.top + 1 >= sprite.old_rect.bottom):
                            self.rect.top = sprite.rect.bottom
                            self.pos.y = self.rect.centery
                            self.vel.y *= -1
            # Predicting landing if collision between obstacles and ball game
            if is_gameball:
                self.game.bot.predict_move()

    def on_air_ball_collision(self, other):
        balls_in_the_air = not self.is_standing() and not other.is_standing()
        if self.circle_2_circle_overlap(other) and balls_in_the_air: 
            x1, x2 = self.pos, other.pos
            m1, m2 = self.r**2, other.r**2
            M = m1 + m2
            R = self.r + other.r
            v1, v2 = self.vel, other.vel
            # The distance has already been computed, can simplify here
            d = pg.math.Vector2.magnitude(x1 - x2)
            disp = (d - R) * 0.5
            n = vec(x2[0] - x1[0], x2[1] - x1[1])  
            # Computing new velocities
            n_v1 = v1 - 2*m2 / M * vec.dot(v1 - v2, x1 - x2) * (x1 - x2) / d**2
            n_v2 = v2 - 2*m1 / M * vec.dot(v2 - v1, x2 - x1) * (x2 - x1) / d**2
            self.vel = n_v1
            other.vel = n_v2
            # Dealing with sticky collisions issues
            self.pos.x += disp * (n.x / d)
            self.pos.y += disp * (n.y / d)
            other.pos.x -= disp * (n.x / d) 
            other.pos.y -= disp * (n.y / d)
            # Predicting ball game landing
            if other == self.game.gameball:
                self.game.bot.predict_move(self == self.game.bot)

    def on_floor_ball_collision(self):
        gameball = self.game.gameball # Sake of readability
        if self.circle_2_circle_overlap(gameball):
            dx, dy = gameball.pos.x - self.pos.x, gameball.pos.y - self.pos.y
            angle = math.atan2(dy, dx)
            # Only the velocity of the ball game is changed
            gameball.vel.x = math.cos(angle) * GAMEBALL_X_ELASTICITY 
            gameball.vel.y *= -1  
            # Dealing with sticky collisions issues
            n = vec(dx, dy)
            R = self.r + gameball.r
            d = pg.math.Vector2.magnitude(gameball.pos - self.pos)
            disp = (d - R) * 0.5
            self.pos.x += disp * (n.x / d)
            self.pos.y += disp * (n.y / d)
            gameball.pos.x -= disp * (n.x / d)
            gameball.pos.y -= disp * (n.y / d)
            # Predicting bot's move
            self.game.bot.predict_move(self == self.game.bot)
            gameball.horizontal_range(gameball.pos.x, HEIGHT - gameball.pos.y, abs(angle))

    def end_round_conditions(self) -> bool:
        # If the ball hits the floor and is in the player/bot zone
        if self == self.game.gameball:
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

    def predict_landing(self):
        self.trajectory.clear()
        x, y = self.pos.x, self.pos.y
        vel_x, vel_y = self.vel.x, self.vel.y
        buffer_rect = pg.Rect(self.pos.x - self.r, self.pos.y - self.r, self.r*2, self.r*2)
        while True:
            vel_y += self.acc.y
            x += vel_x + 0.5 * self.acc.x
            y += vel_y + 0.5 * self.acc.y
            self.trajectory.append((x, y))
            buffer_rect.center = (x, y)
            if buffer_rect.colliderect(self.game.net):
                self.game.bot.ball_landing_point = (WIDTH + NET_WIDTH) * 0.5
                return None
            if y + GAMEBALL_RADIUS >= HEIGHT:
                self.game.bot.ball_landing_point = x
                return None

    def update(self):
        """
        Updates positions and applies collisions (if any)
        """
        is_gameball = (self == self.game.gameball)
        # Rect at previous frame
        self.old_rect = self.rect.copy()
        if self == self.game.player: # Player only
            self.vel.x = 0
            keys = pg.key.get_pressed() # Keyboard events
            if keys[pg.K_RIGHT]:
                self.vel.x += PLAYER_X_SPEED
            elif keys[pg.K_LEFT]:
                self.vel.x += -PLAYER_X_SPEED
        # Updating velocity
        self.vel += self.acc
        # Updating x pos
        self.pos.x += self.vel.x + 0.5 * self.acc.x
        self.rect.centerx = self.pos.x
        # Screen collisions (horitonzal)
        self.screen_collisions("horizontal", is_gameball)
        # Obstacles collisions (horizontal)
        self.obstacles_collisions("horizontal", is_gameball)
        # Updating y pos
        self.pos.y += self.vel.y + 0.5 * self.acc.y
        self.rect.centery = self.pos.y
        # Screen collisions (vertical)
        self.screen_collisions("vertical", is_gameball)
        # Obstacles collisions (vertical)
        self.obstacles_collisions("vertical", is_gameball)       
        # Ball collision (on floor)
        if not is_gameball and self.is_standing():
            self.on_floor_ball_collision()
        else:
            particles = self.game.balls.sprites()
            for i, p in enumerate(particles):
                for other in particles[i+1:]:
                    p.on_air_ball_collision(other)

# GAME BALL -------------------------------------------------
class GameBall(Ball):
    def __init__(self, game, r, x, y, vel, acc, color):
        super().__init__(game, r, x, y, vel, acc, color)

    def horizontal_range(self, x0, y0, angle):
        # Sake of readability
        vel = self.vel.magnitude()
        g = GAMEBALL_GRAVITY
        # Computing the horizontal range
        h_R = vel * cos(angle) 
        h_R *= (vel * sin(angle) + sqrt((vel * sin(angle))**2 + 2 * g * y0)) 
        h_R /= g
        h_R += x0
        print("range=", h_R)
    

# BOT -------------------------------------------------------
class Bot(Ball):
    def __init__(self, game, r, x, y, vel, acc, color):
        super().__init__(game, r, x, y, vel, acc, color)
        self.ball_landing_point = None
        self.can_move = False
        self.direction = 0

    def predict_move(self, self_hit=False):
        self.game.gameball.predict_landing()
        if self.is_in_bot_zone(self.ball_landing_point):
            if self.ball_landing_point > self.game.bot.pos.x:
                self.game.bot.direction = 1
            else:
                self.game.bot.direction = -1 

    def update(self):
        self.vel.x = 0
        if self.ball_landing_point:
            if self.pos.x < self.ball_landing_point and self.direction == -1:
                self.direction = 0
            if self.pos.x > self.ball_landing_point and self.direction == 1:
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

# --------------------------------------------------------------
# Obstacle

class Obstacle(pg.sprite.Sprite):
    def __init__(self, game, x, y, w, h, color, vel):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.pos = vec(x, y)
        self.image = pg.Surface((w, h))
        self.image.fill(color)
        self.vel = vel
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.old_rect = self.rect.copy()
        
    def update(self) -> None:
        if self.vel != vec(0, 0):
            # Old frame rect
            self.old_rect = self.rect.copy()
            # Updating position
            self.pos.y += self.vel.y
            self.rect.center = self.pos
            # Collisions
            self.collisions()

    def collisions(self) -> None:
        # Ceiling collision
        if self.rect.top < 0:
            self.rect.top = 0
            self.pos.y = self.rect.centery
            self.vel.y *= -1
        # Net collision
        if self.rect.colliderect(self.game.net):
            self.rect.bottom = self.game.net.rect.top
            self.pos.y = self.rect.centery
            self.vel.y *= -1
        # Immobile ball collision (those two cases rarely happen)
        if self.rect.colliderect(self.game.player):
            if self.game.player.is_standing(1, False, [self.game.net]):
                self.rect.bottom = self.game.player.rect.top
                self.pos.y = self.rect.centery
                self.vel.y *= -1
            if self.game.player.rect.top < 0:
                self.rect.top = self.game.player.rect.bottom
                self.pos.y = self.rect.centery
                self.vel.y *= -1

def main():
    pass

if __name__ == "__main__":
    main()




