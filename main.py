from cmath import nan
import pygame
import random
import ctypes
import math
import numpy as np

# pygame initialize
pygame.init()

user32 = ctypes.windll.user32
dimensions = (user32.GetSystemMetrics(0), user32.GetSystemMetrics(1))
width = dimensions[0]
height = dimensions[1]

screen = pygame.display.set_mode(dimensions)
clock = pygame.time.Clock()
fps = 60

screen.fill((0, 0, 0))

##colors##
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
white = (255, 255, 255)
black = (0, 0, 0)
##########


class boid:
    def __init__(self, position, velocity, acceleration, size, color):
        self.position = np.array(position)
        self.velocity = np.array(velocity)
        self.size = size
        self.color = color
        self.radius = self.size // 2
        self.acceleration = np.array(acceleration)
        self.maxmag = 5

    def __getitem__(self, item):
        return getattr(self, item)

    def move(self):
        self.velocity += self.acceleration
        self.position += self.velocity
        self.acceleration = np.array([0, 0])

    def check_wall_collision(self):
        xpos = self.position[0]
        ypos = self.position[1]
        radius = self.size // 2

        if xpos < 0 + radius:
            xpos = width - radius
        if xpos > width - radius:
            xpos = 0 + radius
        if ypos < 0 + radius:
            ypos = height - radius
        if ypos > height - radius:
            ypos = 0 + radius

        self.position = np.array([xpos, ypos])

    def draw(self):
        pygame.draw.circle(screen, self.color, self.position, self.size)

    def align(self, all_boids):
        currentboid = self.position
        neighbourvel = np.array([])

        for i in all_boids:
            compareboid = i["position"]
            mag = math.dist(currentboid, compareboid)

            if mag < 50 and np.array_equal(currentboid, compareboid) == False:
                pygame.draw.line(screen, white, currentboid, compareboid, 2)
                temp = neighbourvel
                neighbourvel = np.append(temp, i["velocity"], axis=0)

        desired = np.reshape(neighbourvel, (len(neighbourvel) // 2, 2))
        desired = np.mean(desired, axis=0, dtype=np.int32)
        mag = np.linalg.norm(desired)

        print(desired, desired * np.around(self.maxmag / mag, 0))

        if desired[0] != nan or desired[1] != nan:
            desired *= np.around(self.maxmag / mag, 0)

        # self.acceleration = desired.astype(np.int32) - self.velocity


def spawn():
    x = random.randint(20, width - 20)
    y = random.randint(20, height - 20)
    return np.array([x, y])


def startvel():
    a = -5
    vels = []

    for i in range(1, a * -2):
        a += 1
        if a != 0:
            vels.append(a)

    vx = random.choice(vels)
    vy = random.choice(vels)
    return np.array([vx, vy])


population = 50

p = [boid(spawn(), startvel(), [0, 0], 5, red) for i in range(population)]

run = True

while run:
    clock.tick(fps)
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            run = False
    screen.fill((0, 0, 0))

    for i in range(len(p)):
        p[i].check_wall_collision()
        p[i].move()
        p[i].align(p)
        p[i].draw()

    pygame.display.update()
