import pygame
import random
import math
import numpy as np

width, height = 700, 450
screen = pygame.display.set_mode((width, height))
particles = []
no_particles = 100
tick_speed = 200

class Particle:
    def __init__(self, x, y, r):
        self.r = r
        self.pos = np.array([x, y])
        self.vel = np.array([random.uniform(-0.5, 0.5), random.uniform(-0.5, 0.5)])
        self.acc = np.array([0, 0]) #tick_speed/(tick_speed * 10)

    def display(self):
        pygame.draw.circle(screen, (227, 53, 15), (int(self.pos[0]), int(self.pos[1])), self.r, 1)

    def move(self):
        self.vel = self.vel + self.acc 
        self.pos = self.pos + self.vel
            
    def bounce(self):
        if self.pos[1] > height - self.r:
            self.pos[1] = 2*(height - self.r) - self.pos[1]
            self.vel[1] = -self.vel[1]

        elif self.pos[1] < self.r:
            self.pos[1] = 2*self.r - self.pos[1]
            self.vel[1] = -self.vel[1]

        if self.pos[0] + self.r > width:
            self.pos[0] = 2*(width - self.r) - self.pos[0]            
            self.vel[0] = -self.vel[0]
            
        elif self.pos[0] < self.r:
            self.pos[0] = 2*self.r - self.pos[0]
            self.vel[0] = -self.vel[0]

    @classmethod
    def resolveStatically(cls, n, dc, p1, p2):
          displacement = (dc - p1.r - p2.r) * 0.5
          p1.pos[0] += displacement * (n[0] / dc)
          p1.pos[1] += displacement * (n[1] / dc)
          p2.pos[0] -= displacement * (n[0] / dc)
          p2.pos[1] -= displacement * (n[1] / dc)
            
    @classmethod
    def collision(cls, p1, p2):
        dc = math.hypot((p1.pos[0]-p2.pos[0]), (p1.pos[1]-p2.pos[1]))
        if dc <= p1.r + p2.r:
            x1, y1 = p1.pos[0], p1.pos[1]
            x2, y2 = p2.pos[0], p2.pos[1]
            m1, m2 = p1.r**2, p2.r**2
            
            n = np.array([x2-x1, y2-y1])
            cls.resolveStatically(n, dc, p1, p2)
            
            un = n / np.linalg.norm(n)
            ut = np.array([-un[1], un[0]])
            
            v1 = p1.vel
            v2 = p2.vel

            v1n = np.dot(un, v1)
            v1t = np.dot(ut, v1)

            v2n = np.dot(un, v2)
            v2t = np.dot(ut, v2)

            v1n_prime_s = (v1n * (m1 - m2) + 2*m2*v2n) / (m1 + m2)
            v2n_prime_s = (v2n * (m2 - m1) + 2*m1*v1n) / (m1 + m2)
             
            v1n_prime = v1n_prime_s * un
            v1t_prime = v1t * ut

            v2n_prime = v2n_prime_s * un
            v2t_prime = v2t * ut
            
            u1 = v1n_prime + v1t_prime 
            u2 = v2n_prime + v2t_prime
            p1.vel = u1
            p2.vel = u2

            
while len(particles) < no_particles:
    r = random.randint(10, 20)
    x = random.randint(r, width-r)
    y = random.randint(r, height-r)
    collide = False
    for particle in particles:
        d = (particle.pos[0] - x)**2 + (particle.pos[1] - y)**2
        if d < (r + particle.r)**2:
            collide = True
            break
        
    if not collide:
        particles.append(Particle(x, y, random.randint(10, 20)))
        
          
running = True
clock = pygame.time.Clock()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
    screen.fill((255, 255, 255))

    for i in range(len(particles)):
        particles[i].move()
        particles[i].bounce()
        for j in range(i + 1, len(particles)):
            particles[i].collision(particles[i], particles[j])
        particles[i].display() 
            
    pygame.display.flip()
    clock.tick(tick_speed)

pygame.quit()
quit()