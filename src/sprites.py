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
    def __init__(self, x, y, color):
        """Constructor.
        """
        pg.sprite.Sprite.__init__(self)
        self.image = PLAYERS_ID[color]
        self.rect = self.image.get_rect()
        self.rect.midbottom = x, y
        if x < WIDTH / 2:
            self.left_border = PLAYER_SIZE / 2
            self.right_border = WIDTH / 2 - NET_WIDTH / 2 - PLAYER_SIZE / 2
        self.pos = vec(x, y)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        
    def update(self):
        self.vel = vec(0, 0)
        keys = pg.key.get_pressed()
        if keys[pg.K_RIGHT]:
            self.vel.x += PLAYER_X_SPEED
        elif keys[pg.K_LEFT]:
            self.vel.x += -PLAYER_X_SPEED
            
        self.acc += self.vel * PLAYER_FRICTION
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        
        if self.pos.x < self.left_border:
            self.pos.x = self.left_border
        elif self.pos.x > self.right_border:
            self.pos.x = self.right_border
        self.rect.midbottom = self.pos
               
    # Methods
    # -------
    def move(self, direction) -> None:
        """TODO"""
        current_x = self.rect.midbottom[0]
        max_left_reached = current_x - PLAYER_SIZE / 2 < self.left_border
        max_right_reached = current_x + PLAYER_SIZE / 2 > self.right_border
        if not max_left_reached and not max_right_reached:
            self.rect.move_ip(direction * SPEED, 0)
        else:
            # To create a small "collision" effect at the borders
            self.rect.move_ip(1, 0) if max_left_reached else self.rect.move_ip(-1, 0) 
                
    def jump(self) -> None:
        pass
    
    def display_player(self, screen):
        pass
        
# --------------------------------------------------------------

#Net
class Net(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((NET_WIDTH, NET_HEIGHT))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT - NET_HEIGHT / 2)

def main():
    g = Player(0, 0, "GREEN")
    g.acc.x = 5

if __name__ == "__main__":
    main()




