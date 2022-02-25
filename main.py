from cv2 import compare
import pygame
import random
import ctypes
import math

from pyparsing import White

# pygame initialize
pygame.init()

user32 = ctypes.windll.user32
dimensions = (user32.GetSystemMetrics(0), user32.GetSystemMetrics(1))
width = dimensions[0]
height = dimensions[1]

screen = pygame.display.set_mode(dimensions)
clock = pygame.time.Clock()
fps = 75

screen.fill((0,0,0))

##colors##
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
white = (255,255,255)
##########

class boid():
    def __init__(self, position, velocity, size, color):
        self.position = position
        self.velocity = velocity
        self.size = size
        self.color = color
        self.radius = self.size//2
    
    def __getitem__(self, item):
        return getattr(self, item)

    def move(self):
        self.position = [(self.velocity[0]+self.position[0]), (self.velocity[1]+self.position[1])]
        
    # def check_wall_collision(self):
    #     xpos = self.position[0]
    #     ypos = self.position[1]
    #     xvel = self.velocity[0]
    #     yvel = self.velocity[1]
    #     radius = self.size//2

    #     if (xpos <= 0+radius) or (xpos >= width-radius):
    #         xvel *= -1
    #     if (ypos <= 0+radius) or (ypos >= height-radius):
    #         yvel *= -1

    #     self.velocity = [xvel, yvel]

    def check_wall_collision(self):
        xpos = self.position[0]
        ypos = self.position[1]
        xvel = self.velocity[0]
        yvel = self.velocity[1]
        radius = self.size//2

        if xpos < 0+radius:
            xpos = width-radius
        if xpos > width-radius:
            xpos = (0+radius)
        if ypos < 0+radius:
            ypos = height-radius
        if ypos > height-radius:
            ypos = (0+radius)

        self.position = [xpos,ypos]

    def draw(self):
        x = self.position[0]
        y = self.position[1]
        coords = (x, y)
        pygame.draw.circle(screen, self.color, coords, self.size)
    
    def steer(self, all_boids):
        currentboid = self.position
        for i in all_boids:
            compareboid = i['position']
            if math.sqrt(((currentboid[0]-compareboid[0])**2)+((currentboid[1]-compareboid[1])**2)) < 100:
                pygame.draw.line(screen, white, currentboid, compareboid, 2)
                # self.velocity = i['velocity']

def spawn():
    x = random.randint(20, width-20)
    y = random.randint(20, height-20)
    return [x,y]

def startvel():
    a = -3
    vels = []

    for i in range(1, a*-2):
        a+=1
        if a != 0:
            vels.append(a)

    vx = random.choice(vels)
    vy = random.choice(vels)
    return [vx,vy]

population = 100

p = [boid(spawn(), startvel(), 5, red) for i in range(population)]

run = True

while run:
    clock.tick(fps)
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            run = False
    screen.fill((0,0,0))

    for i in range(len(p)):
        p[i].check_wall_collision()
        p[i].move()
        p[i].steer(p)
        p[i].draw()
        

    pygame.display.update()
