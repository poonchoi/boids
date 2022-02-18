import pygame
import numpy



class boid():
    def __init__(self, position, velocity, size, color):
        self.position = [0,0]
        self.velocity = [3,1]

    def move(self):
        self.position = [(self.velocity[0]+self.position[0]), (self.velocity[1]+self.position[1])]
        
    def check_collision(self):
        pass

    def draw(self):
        x = self.position[0]
        y = self.position[1]
        coords = (x, y)