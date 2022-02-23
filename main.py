import pygame
from pygame.locals import *
import numpy

# # pygame initialize
# pygame.init()

# dimensions = (1920,1080)
# width = dimensions[0]//2
# height = dimensions[1]//2

# screen = pygame.display.set_mode(dimensions)
# clock = pygame.time.Clock()
# fps = 75

# screen.fill((0,0,0))

# class boid():
#     def __init__(self, position, velocity, size, color):
#         self.position = [0,0]
#         self.velocity = [3,1]
#         self.size = 1
#         self.color = (255,255,255)

#     def move(self):
#         self.position = [(self.velocity[0]+self.position[0]), (self.velocity[1]+self.position[1])]
        
#     def check_collision(self):
#         if 0 < self.position[0] < 1080:
#             self.position[1] *= -1
#         if 0 < self.position[1] < 1920:
#             self.position[0] *= -1

#     def draw(self):
#         x = self.position[0]
#         y = self.position[1]
#         coords = (x, y)
#         pygame.draw.circle(screen, self.color, coords, self.size)


# population = 1
# p = [boid([0,0], [3,1], 5, (255,255,255)) for i in range(population)]

# run = True

# while run:
#     clock.tick(fps)
#     for i in pygame.event.get():
#         if i.type == pygame.QUIT:
#             run = False
#     screen.fill((0,0,0))

#     for i in p:
#         i.check_collision()
#         i.move()
#         i.draw()

# pygame initialize
pygame.init()

dimensions = 500,500
width = dimensions[0]//2
height = dimensions[1]//2

screen = pygame.display.set_mode(dimensions)
clock = pygame.time.Clock()
fps = 75

screen.fill(255)

run = True

color = (255,255,255)
coords = width, height
size = 5

while run:
    clock.tick(fps)
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            run = False

    pygame.draw.circle(screen, color, coords, size)
    pygame.display.update()

pygame.quit()
