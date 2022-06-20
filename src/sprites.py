"""
Sprites classes
"""

import math
import pygame as pg
import numpy as np

from itertools import cycle
from settings import *
vec = pg.math.Vector2

# --------------------------------------------------------------

# Player
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
        self.m = 3 # ??
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
       
    def jump(self) -> None:  
        # Can only jump on platforms or floor
        if self.is_standing(PLAYER_JUMP_TOLERANCE, True, self.game.obstacles): 
            self.vel.y = PLAYER_Y_SPEED
        
    def screen_collisions(self, orientation, is_ball_game) -> None:
        """
        Deals with screen collisions (left/right/top/bottom borders)
        """
        if orientation == "horizontal":
            # Right border
            if self.rect.right > WIDTH:
                self.rect.right = WIDTH
                self.pos.x = self.rect.centerx
                if is_ball_game:
                    self.vel.x *= -1
            # Left border
            elif self.rect.left < 0:
                self.rect.left = 0
                self.pos.x = self.rect.centerx
                if is_ball_game:
                    self.vel.x *= -1
        if orientation == "vertical":
            # Bottom border
            if self.rect.bottom >= HEIGHT:
                self.rect.bottom = HEIGHT
                self.pos.y = self.rect.centery
                if is_ball_game:
                    self.vel.y *= -1
                else:
                    self.vel.y = 0
            # Top border
            elif self.rect.top < 0:
                self.rect.top = 0
                self.pos.y = self.rect.centery
                self.vel.y *= -1

    def obstacles_collisions(self, orientation, is_ball_game):
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
                            if is_ball_game: self.vel.x *= -1
                    # Left side collision
                    if (self.rect.left <= sprite.rect.right and 
                        self.old_rect.left + 1 >= sprite.old_rect.right):
                            self.rect.left = sprite.rect.right
                            self.pos.x = self.rect.centerx
                            if is_ball_game: self.vel.x *= -1
            for sprite in collisions_sprites:
                if orientation == "vertical":
                    # Top side collision
                    if (self.rect.bottom >= sprite.rect.top and 
                        self.old_rect.bottom - 1 <= sprite.old_rect.top):
                            self.rect.bottom = sprite.rect.top
                            self.pos.y = self.rect.centery
                            if is_ball_game: 
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
            if is_ball_game:
                self.predict_landing()

    def on_floor_ball_collision(self, ball_game):
        if self.circle_2_circle_overlap(ball_game):
            print("BOOM")
            dx, dy = ball_game.pos.x - self.pos.x, ball_game.pos.y - self.pos.y
            angle = math.atan2(dy, dx)
            # Only the velocity of the ball game is changed
            ball_game.vel.x = math.cos(angle) * BALL_GAME_X_ELASTICITY 
            ball_game.vel.y *= -1  
            # Dealing with sticky collisions issues
            n = vec(dx, dy)
            R = self.r + ball_game.r
            d = pg.math.Vector2.magnitude(ball_game.pos - self.pos)
            disp = (d - R) * 0.5
            self.pos.x += disp * (n.x / d)
            self.pos.y += disp * (n.y / d)
            ball_game.pos.x -= disp * (n.x / d)
            ball_game.pos.y -= disp * (n.y / d)
            ball_game.predict_landing()


    def end_round_conditions(self) -> bool:
        player_zone = (WIDTH - NET_WIDTH) * 0.5 - PLAYER_RADIUS
        bot_zone =  (WIDTH + NET_WIDTH) * 0.5 + BOT_RADIUS
        # If the ball hits the floor and is in the player/bot zone
        if self == self.game.ball_game:
            if self.is_standing():
                if self.pos.x >= bot_zone:
                    self.game.scores["Player"] += 1
                elif self.pos.x <= player_zone:
                    self.game.scores["Bot"] += 1
                return True
        # If player/bot goes into its wrong zone
        else:
            if self == self.game.bot and self.pos.x <= player_zone:
                self.game.scores["Player"] += 1
                return True
            elif self == self.game.player and self.pos.x >= bot_zone:
                self.game.scores["Bot"] += 1
                return True
        return False

    def predict_landing(self):
        landing = False
        x, y = self.pos.x, self.pos.y
        vel_x, vel_y = self.vel.x, self.vel.y
        while not landing:
            vel_y += self.acc.y
            x += vel_x + 0.5 * self.acc.x
            y += vel_y + 0.5 * self.acc.y
            if y + BALL_GAME_RADIUS >= HEIGHT:
                landing = True
        # The ball must hit the floor and land in the bot-zone...
        # ...ie the right part on the pitch
        if landing and x > (WIDTH + NET_WIDTH) * 0.5:
            self.game.bot.ball_landing_point = x
            if x - self.game.bot.pos.x > 0:
                self.game.bot.direction = 1
            else:
                self.game.bot.direction = -1 

    def update(self):
        """
        Updates positions and applies collisions (if any)
        """
        is_ball_game = (self == self.game.ball_game)
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
        self.screen_collisions("horizontal", is_ball_game)
        # Obstacles collisions (horizontal)
        self.obstacles_collisions("horizontal", is_ball_game)
        # Updating y pos
        self.pos.y += self.vel.y + 0.5 * self.acc.y
        self.rect.centery = self.pos.y
        # Screen collisions (vertical)
        self.screen_collisions("vertical", is_ball_game)
        # Obstacles collisions (vertical)
        self.obstacles_collisions("vertical", is_ball_game)       
        # Ball collision (on floor)
        if not is_ball_game and self.is_standing():
            self.on_floor_ball_collision(self.game.ball_game)


# --------------------------------------------------------------
# Bot

class Bot(Ball):
    def __init__(self, game, r, x, y, vel, acc, color):
        super().__init__(game, r, x, y, vel, acc, color)
        self.ball_landing_point = None
        self.direction = 0

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
                self.on_floor_ball_collision(self.game.ball_game)

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




