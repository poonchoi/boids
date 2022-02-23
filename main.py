import pygame
import random

# pygame initialize
pygame.init()

dimensions = (1920,1080)
width = dimensions[0]
height = dimensions[1]

screen = pygame.display.set_mode(dimensions)
clock = pygame.time.Clock()
fps = 75

screen.fill((0,0,0))

class boid():
    def __init__(self, position, velocity, size, color):
        self.position = position
        self.velocity = velocity
        self.size = size
        self.color = color
        self.radius = self.size//2

    def move(self):
        self.position = [(self.velocity[0]+self.position[0]), (self.velocity[1]+self.position[1])]
        
    def check_collision(self):
        xpos = self.position[0]
        ypos = self.position[1]
        xvel = self.velocity[0]
        yvel = self.velocity[1]
        radius = self.size//2

        if (xpos <= 0+radius) or (xpos >= width-radius):
            xvel *= -1
        if (ypos <= 0+radius) or (ypos >= height-radius):
            yvel *= -1
        
        self.velocity = [xvel, yvel]

    def draw(self):
        x = self.position[0]
        y = self.position[1]
        coords = (x, y)
        pygame.draw.circle(screen, self.color, coords, self.size)


def spawn():
    vels = [5, 4, 3, 2, 1, -1, -2, -3, -4, -5]
    x = random.randint(1, width-1)
    y = random.randint(1, height-1)
    vx = random.choice(vels)
    vy = random.choice(vels)
    return x, y, vx, vy

population = 1000

p = [boid([random.randint(0,width),random.randint(0,height)],[random.randint(-2,2),random.randint(-2,2)],7,(255,255,255)) for i in range(population)]

run = True

while run:
    clock.tick(fps)
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            run = False
    screen.fill((0,0,0))

    for i in p:
        i.check_collision()
        i.move()
        i.draw()
    pygame.display.update()
