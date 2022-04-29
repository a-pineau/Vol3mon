"""
Sprites classes
"""

from ipaddress import NetmaskValueError
import pygame as pg
from settings import *
vec = pg.math.Vector2

# --------------------------------------------------------------

# Player
class Player(pg.sprite.Sprite):
    """
    A class used to represent a standard Abalone board.
    Both players have 14 marbles.
    A player loses whenever 6 of his marbles are out.
    
    Attributes
    ----------

    Methods
    -------
    """
    # Constructor
    # -----------
    def __init__(self, game, x, y, color):
        """Constructor.
        """
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.image = PLAYERS_ID[color]
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width / 2)
        pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.pos = vec(x, y)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.rect.center = self.pos
        
    def update(self):
        self.vel.x = 0
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
    
        # ??
        any_but_current = pg.sprite.Group()
        for element in self.game.all_sprites:
            if element != self and element != self.game.ball_game:
                any_but_current.add(element)
    
        # x-collisions with platforms
        hits = pg.sprite.spritecollide(self, any_but_current, False)
        if hits:
            # Hitting left border of a platform
            if self.vel.x > 0:
                self.rect.right = hits[0].rect.left
                self.pos.x = self.rect.centerx
            # Hitting right border of a platform
            elif self.vel.x < 0:
                self.rect.left = hits[0].rect.right
                self.pos.x = self.rect.centerx

        # Updating y pos
        self.pos.y += self.vel.y + 0.5 * self.acc.y
        self.rect.centery = self.pos.y

        # y-collisions with platforms
        hits = pg.sprite.spritecollide(self, any_but_current, False)
        if hits:
            # Falling, hitting top of a platform
            if self.vel.y > 0:
                self.rect.bottom = hits[0].rect.top
                self.pos.y = self.rect.centery
                self.vel.y *= 0
            # Jumping, hitting bottom of a platform
            elif self.vel.y < 0:
                self.rect.top = hits[0].rect.bottom
                self.pos.y = self.rect.centery
                self.vel.y = 0
    
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
 
# --------------------------------------------------------------
# BallGame

class BallGame(Player):
    def __init__(self, game, x, y, color):
        super().__init__(game, x, y, color)
        self.acc = vec(0, BALL_GRAVITY)
        self.vel = vec(0, 0)

    def update(self):        
        # Updating velocity
        self.vel += self.acc
        print(self.vel)
        # Updating x pos
        self.pos += self.vel + 0.5 * self.acc
        self.rect.center = self.pos
        
        # Collision with floor (need to take gravity into account)
        if self.rect.bottom > self.game.p_floor.rect.top:
            self.rect.bottom = self.game.p_floor.rect.top
            self.pos.y = self.rect.centery
            self.vel.y *= -1
        # Collision with ceiling
        elif self.rect.top < 0:
            self.vel.y *= -1
        # Collision with left/right borders
        elif self.rect.left < 0 or self.rect.right > WIDTH:
            self.vel.x *= -1
            
        # Collision with the net and the moving platform
        obstacles = pg.sprite.Group(self.game.p_net)
        hits = pg.sprite.spritecollide(self, obstacles, False)
        if hits:
            # The conditions on velocity is used to avoid glitchs when collisions between 2 moving rectangles occur
            # Top collision
            if abs(hits[0].rect.top - self.rect.bottom) < COLLISION_TOLERANCE and self.vel.y > 0: 
                self.vel.y *= -1            
            # Bottom collision
            if abs(hits[0].rect.bottom - self.rect.top) < COLLISION_TOLERANCE and self.vel.y < 0: 
                self.vel.y *= -1
            # Right collision
            if abs(hits[0].rect.right - self.rect.left) < COLLISION_TOLERANCE and self.vel.x < 0: 
                self.vel.x *= -1
            # Left collision
            if abs(hits[0].rect.left - self.rect.right) < COLLISION_TOLERANCE and self.vel.x > 0:
                self.vel.x *= -1
        
        # Collision with players
        v_ball_game = vec(self.rect.x, self.rect.y)
        v_player = vec (self.game.player.rect.x, self.game.player.rect.y)
        r_ball_game = self.radius
        r_player = self.game.player.radius
        if pg.sprite.collide_circle(self, self.game.player):
            if self.rect.bottom > self.game.player.rect.top:
                self.rect.bottom = self.game.player.rect.top
                self.pos.y = self.rect.centery
            new_vec = v_player - v_ball_game
            self.vel = vec(self.vel.x, self.vel.y).reflect(new_vec)

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
        
    def update(self) -> None:
        self.pos.y += self.vel.y + 0.5 * self.acc.y
        self.rect.center = self.pos
        
        # y-collisions with all stuffs
        if self.game:
            if self.rect.colliderect(self.game.p_net) or self.rect.top < 0:
                self.vel.y *= -1
                
                
def main():
    pass

if __name__ == "__main__":
    main()




