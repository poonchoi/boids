import pygame
import random
import ctypes
import math
import numpy as np

##GLOBALS##
VISION = 50
population = 100
boidsize = 3
MAX_SPEED = 5
###########

##COLORS##
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
white = (255, 255, 255)
black = (0, 0, 0)
##########

##PYGAME INIT##
pygame.init()

user32 = ctypes.windll.user32
dimensions = (user32.GetSystemMetrics(0), user32.GetSystemMetrics(1))
width = dimensions[0]
height = dimensions[1]

screen = pygame.display.set_mode(dimensions)
clock = pygame.time.Clock()
fps = 60

screen.fill(black)
###############


class Boid:
    def __init__(self, position, velocity, diameter, color):
        self.position = np.array(position, dtype=float)
        self.velocity = np.array(velocity, dtype=float)
        self.acceleration = np.array([0, 0], dtype=float)
        self.diameter = diameter
        self.radius = diameter // 2
        self.color = color

    def __getitem__(self, item):
        return getattr(self, item)

    def move(self):
        self.position += self.velocity + self.acceleration
        self.acceleration = np.array([0, 0], dtype=float)

    def draw(self):
        pygame.draw.circle(screen, self.color, self.position, self.diameter)

    def wall_check(self):
        xpos = self.position[0]
        ypos = self.position[1]
        leftb = 0 + self.radius
        rightb = width - self.radius
        topb = 0 + self.radius
        botb = height - self.radius

        if xpos <= leftb:
            xpos = rightb
        elif xpos >= rightb:
            xpos = leftb
        if ypos <= topb:
            ypos = botb
        elif ypos >= botb:
            ypos = topb

        self.position = np.array([xpos, ypos], dtype=float)

    def alignment(self, all_boids):
        currentpos = self.position
        desiredvels = np.empty((0, 2))
        for i in all_boids:
            otherpos = i["position"]
            othervel = i["velocity"]
            mag = math.dist(currentpos, otherpos)

            if mag <= VISION and not (np.array_equal(currentpos, otherpos)):
                desiredvels = np.append(desiredvels, othervel)
                pygame.draw.line(screen, white, currentpos, otherpos, 1)

        if len(desiredvels) > 2:
            desiredvels = np.reshape(desiredvels, (len(desiredvels) // 2, 2))
            avg = np.average(desiredvels, axis=0)
            avg *= MAX_SPEED / np.linalg.norm(avg)
            self.acceleration = avg - self.velocity
        elif len(desiredvels) == 2:
            avg = desiredvels
            avg *= MAX_SPEED / np.linalg.norm(avg)
            self.acceleration = avg - self.velocity
        else:
            avg = np.array([0, 0], dtype=float)
            self.acceleration = avg

    def separation(self):
        pass

    def cohesion(self, all_boids):
        currentpos = self.position
        desiredposs = np.empty((0, 2))
        for i in all_boids:
            otherpos = i["position"]
            mag = math.dist(currentpos, otherpos)
            if mag <= VISION and not (np.array_equal(currentpos, otherpos)):
                desiredposs = np.append(desiredposs, otherpos)

        if len(desiredposs) > 2:
            desiredposs = np.reshape(desiredposs, (len(desiredposs) // 2, 2))
            avg = np.average(desiredposs, axis=0)
            avg *= MAX_SPEED / np.linalg.norm(avg)
            mag = math.dist(avg, self.position)
            self.acceleration = -avg
        elif len(desiredposs) == 2:
            avg = desiredposs
            avg *= MAX_SPEED / np.linalg.norm(avg)
            mag = math.dist(avg, self.position)
            self.acceleration = -avg
        else:
            avg = np.array([0, 0], dtype=float)
            self.acceleration = -avg


def spawn():
    x = random.randint(20, width - 20)
    y = random.randint(20, height - 20)
    return np.array([x, y], dtype=float)


def startvel():
    a = -5
    vels = []

    for i in range(1, a * -2):
        a += 1
        if a != 0:
            vels.append(a)

    vx = random.choice(vels)
    vy = random.choice(vels)
    return np.array([vx, vy], dtype=float)


def main():

    p = [Boid(spawn(), startvel(), boidsize, green) for i in range(population)]

    run = True

    while run:
        clock.tick(fps)
        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                run = False
        screen.fill(black)

        for i in range(len(p)):
            p[i].wall_check()
            p[i].move()
            p[i].alignment(p)
            # p[i].cohesion(p)
            p[i].draw()

        pygame.display.update()


if __name__ == "__main__":
    main()
