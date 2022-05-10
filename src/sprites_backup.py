"""
Sprites classes
"""

import math
import pygame as pg
from copy import deepcopy
from settings import *
vec = pg.math.Vector2

# --------------------------------------------------------------

# Player
class Player(pg.sprite.Sprite):
    # -----------
    def __init__(self, game, x, y, color):
        """Constructor.
        """
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.image = PLAYERS_ID[color]
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width / 2)
        self.pos = vec(x, y)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.m = 3
        self.rect.center = self.pos
        
    def update(self):
        balls = pg.sprite.Group()
        for sprite in self.game.balls:
            if sprite != self:
                balls.add(sprite) 
        # Checking if objets are colliding already
        previous_collisions = pg.sprite.spritecollide(self, balls, False, pg.sprite.collide_circle)
        
        self.vel = vec(2, 0)
        self.acc = vec(0, PLAYER_GRAVITY)
        keys = pg.key.get_pressed()
        if keys[pg.K_RIGHT]:
            self.vel.x += PLAYER_X_SPEED
        elif keys[pg.K_LEFT]:
            self.vel.x += -PLAYER_X_SPEED
        
        # Updating velocity
        self.vel += self.acc
        
        # Updating x pos
        self.pos.x += self.vel.x + 0.5 * self.acc.x
        self.rect.centerx = self.pos.x
        
        # Left and right borders
        if self.rect.left < 0:
            self.rect.left = 0
            self.pos.x = self.rect.centerx
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
            self.pos.x = self.rect.centerx
    
        # # x-collisions with platforms
        # hits = pg.sprite.spritecollide(self, self.game.platforms, False)
        # if hits:
        #     # Hitting left border of a platform
        #     if self.vel.x > 0:
        #         self.rect.right = hits[0].rect.left
        #         self.pos.x = self.rect.centerx
        #     # Hitting right border of a platform
        #     elif self.vel.x < 0:
        #         self.rect.left = hits[0].rect.right
        #         self.pos.x = self.rect.centerx

        # Updating y pos
        self.pos.y += self.vel.y + 0.5 * self.acc.y
        self.rect.centery = self.pos.y

        # y-collisions with platforms
        # hits = pg.sprite.spritecollide(self, self.game.platforms, False)
        # if hits:
        #     # Falling, hitting top of a platform
        #     if self.vel.y > 0:
        #         self.rect.bottom = hits[0].rect.top
        #         self.pos.y = self.rect.centery
        #         self.vel.y *= 0
        #     # Jumping, hitting bottom of a platform
        #     elif self.vel.y < 0:
        #         self.rect.top = hits[0].rect.bottom
        #         self.pos.y = self.rect.centery
        #         self.vel.y = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
            self.pos.y = self.rect.centery
            self.vel.y = 0
            
        new_collisions = pg.sprite.spritecollide(self, balls, False, pg.sprite.collide_circle)
        if new_collisions and not previous_collisions:
            self.ellastic_collision(self.game.player)
            
    def standing_on_platform(self) -> bool:
        self.rect.y += 1
        hits = pg.sprite.spritecollide(self, self.game.platforms, False)   
        self. rect.y -= 1
        if hits:
            return True
        return False
       
    def jump(self) -> None:  
        if self.standing_on_platform(): # Can only jump on platforms
            self.vel.y = PLAYER_Y_SPEED
            
    def ellastic_collision(self, p2):
        new_velx_p1 = ((self.m -  p2.m) * self.vel.x + 2 * p2.m * p2.vel.x) / (self.m + p2.m)
        new_velx_p2 = ((2 * self.m * self.vel.x) - (self.m - p2.m) * p2.vel.x) / (self.m + p2.m)
        self.vel.x = new_velx_p1
        p2.vel.x = new_velx_p2
 
# --------------------------------------------------------------
# BallGame

class BallGame(Player):
    def __init__(self, game, x, y, color, velocity):
        super().__init__(game, x, y, color)
        self.acc = vec(0, 0)
        self.vel = vec(velocity)

    def update(self):       
        balls = pg.sprite.Group()
        for sprite in self.game.balls:
            if sprite != self: balls.add(sprite) 
        # Checking if objets are colliding already
        previous_collisions = pg.sprite.spritecollide(self, balls, False, pg.sprite.collide_circle)
         
        # Updating velocity
        self.vel += self.acc
        # Updating x pos
        self.pos += self.vel + 0.5 * self.acc
        self.rect.center = self.pos
        # Collision with floor (need to take gravity into account)
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
            self.pos.y = self.rect.centery
            self.vel.y *= -1 * BALL_FRICTION
        # Collision with ceiling
        elif self.rect.top < 0:
            self.vel.y *= -1
        # Collision with left/right borders
        elif self.rect.left < 0 or self.rect.right > WIDTH:
            self.vel.x *= -1
            
        # Collision with the net and the moving platform
        # current_collisions = pg.sprite.spritecollide(self, obstacles, False)
        # if current_collisions:
        #     obstacle = current_collisions[0]
        #     # The conditions on velocity is used to avoid glitchs when collisions between 2 moving rectangles occur
        #     # Top collision
        #     if abs(obstacle.rect.top - self.rect.bottom) < COLLISION_TOLERANCE and self.vel.y > 0: 
        #         self.vel.y *= -1            
        #     # Bottom collision
        #     if abs(obstacle.rect.bottom - self.rect.top) < COLLISION_TOLERANCE and self.vel.y < 0: 
        #         self.vel.y *= -1
        #     # Right collision
        #     if abs(obstacle.rect.right - self.rect.left) < COLLISION_TOLERANCE and self.vel.x < 0: 
        #         self.vel.x *= -1
        #     # Left collision
        #     if abs(obstacle.rect.left - self.rect.right) < COLLISION_TOLERANCE and self.vel.x > 0:
        #         self.vel.x *= -1
        
        # Collision with players
        new_collisions = pg.sprite.spritecollide(self, balls, False, pg.sprite.collide_circle)
        if new_collisions and not previous_collisions:
            self.ellastic_collision(new_collisions[0])
        

        # 2
        # v_ball_game = vec(self.rect.x, self.rect.y)
        # v_player = vec (self.game.player.rect.x, self.game.player.rect.y)
        # r_ball_game = self.radius
        # r_player = self.game.player.radius
        # if v_ball_game.distance_to(v_player) < r_ball_game + r_player:
        #     print("Hit")
        #     new_vec = v_player - v_ball_game
        #     self.vel = vec(self.vel.x, self.vel.y).reflect(new_vec)
        #     print(self.vel)
            # self.rect.bottom = self.game.player.rect.top
            # self.pos.y = self.rect.centery
            

# --------------------------------------------------------------
# Platform

class Platform(pg.sprite.Sprite):
    def __init__(self, x, y, w, h, color, vel_x, vel_y, game=None):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((w, h))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.pos = vec(x, y)
        self.vel = vec(vel_x, vel_y)
        self.acc = vec(0, 0)
        self.rect.center = self.pos
        self.game = game
        self.m = 1
        
    def update(self) -> None:
        self.pos.y += self.vel.y + 0.5 * self.acc.y
        self.rect.center = self.pos
        
        # y-collisions with all stuffs
        if self.game:
            if self.rect.colliderect(self.game.p_net) or self.rect.top < 0:
                self.vel.y *= -1
                
                
def main():
    sign = lambda x: math.copysign(1, x)
    print(sign(-1))

if __name__ == "__main__":
    main()




