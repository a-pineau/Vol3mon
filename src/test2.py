import pygame
import random
import os
FILE_DIR = os.path.dirname(__file__)
class Ball(pygame.sprite.Sprite):

    def __init__(self, startpos, velocity, startdir):
        super().__init__()
        self.pos = pygame.math.Vector2(startpos)
        self.velocity = velocity
        self.dir = pygame.math.Vector2(startdir).normalize()
        self.image = pygame.image.load(os.path.join(FILE_DIR, "small_ball.png")
    ).convert_alpha()
        self.rect = self.image.get_rect(center = (round(self.pos.x), round(self.pos.y)))

    def reflect(self, NV):
        self.dir = self.dir.reflect(pygame.math.Vector2(NV))

    def update(self):
        self.pos += self.dir * self.velocity
        self.rect.center = round(self.pos.x), round(self.pos.y)

        if self.rect.left <= 0:
            self.reflect((1, 0))
            self.rect.left = 0
        if self.rect.right >= 700:
            self.reflect((-1, 0))
            self.rect.right = 700
        if self.rect.top <= 0:
            self.reflect((0, 1))
            self.rect.top = 0
        if self.rect.bottom >= 700:
            self.reflect((0, -1))
            self.rect.bottom = 700

pygame.init()
window = pygame.display.set_mode((700, 700))
pygame.display.set_caption('noname')
clock = pygame.time.Clock()

all_balls = pygame.sprite.Group()

start, velocity, direction = (350, 0), 50, (-1, -1)
ball_1 = Ball(start, velocity, direction)

start, velocity, direction = (350, 700), 0, (random.random(), random.random())
ball_2 = Ball(start, velocity, direction)

all_balls.add(ball_1, ball_2)

def reflectBalls(ball_1, ball_2):
    v1 = pygame.math.Vector2(ball_1.rect.center)
    v2 = pygame.math.Vector2(ball_2.rect.center)
    r1 = ball_1.rect.width // 2
    r2 = ball_2.rect.width // 2
    d = v1.distance_to(v2)
    if d < r1 + r2 - 2:
        dnext = (v1 + ball_1.dir).distance_to(v2 + ball_2.dir)
        nv = v2 - v1
        if dnext < d and nv.length() > 0:
            ball_1.reflect(nv)
            ball_2.reflect(nv)

run = True
while run:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    all_balls.update()

    ball_list = all_balls.sprites()
    for i, b1 in enumerate(ball_list):
        for b2 in ball_list[i+1:]:
            reflectBalls(b1, b2)

    window.fill(0)
    pygame.draw.rect(window, (255, 0, 0), (0, 0, 700, 700), 1)
    all_balls.draw(window)
    pygame.display.flip()