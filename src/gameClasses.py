import pyglet
import random
from pyglet import shapes
import numpy
from scipy.spatial import distance
class Movable(pyglet.sprite.Sprite):

    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)



class Dot(pyglet.shapes.Circle):


    def __init__(self, width, height, *args, **kwargs):
        x = random.random() * width
        y = random.random() * height
        super().__init__(x, y, 10, color=(255, 0, 0))

        print("drawn")
        self.draw()


    def collision(self, pos, radius):
        dist = distance.euclidean(self.position, pos)
        if dist <= self.radius + radius:
            return True
        return False






