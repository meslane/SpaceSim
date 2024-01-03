import pygame
from math import *

class Starmap:
    def __init__(self, size):
        self.map = pygame.Surface(size)
        self.stars = []
        
        #camera params
        self.camera_position = vec3(0,0,500)
        self.camera_orientation = [0,0,0]
        self.canvas_position = vec3(0,0,600)
        
    def draw_starmap(self):
        self.map.fill((0,0,0))
        
        for star in self.stars:
            star.distance = distance(star, self.camera_position)
        
        self.stars.sort(key = lambda x: x.distance, reverse = True) #python's sort method is faster than inorder insertion
        
        for star in self.stars:
            pygame.draw.circle(self.map, 
                                star.color, 
                                star.project(self.camera_position, 
                                            self.camera_orientation, 
                                            self.canvas_position),
                                star.size)
        
class vec3:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        
    def __add__(self, other): #addition/subtraction operators
        return point(self.x + other.x, self.y + other.y, self.z + other.z)
    
    def __sub__(self, other):
        return point(self.x - other.x, self.y - other.y, self.z - other.z)
        
    def __truediv__(self, other): #overload operators for scalar multiplication/division
        return point(self.x / other, self.y / other, self.z / other)
        
    def __mul__(self, other):
        return point(self.x * other, self.y * other, self.z * other)
        
    def __iadd__(self, other):
        self.x += other.x
        self.y += other.y
        self.z += other.z
        
        return self
        
    def __isub__(self, other):
        self.x -= other.x
        self.y -= other.y
        self.z -= other.z
        
        return self
        
    def __imul__(self, other):
        self.x *= other
        self.y *= other
        self.z *= other
        
        return self
        
    def __itruediv__(self, other):
        self.x /= other
        self.y /= other
        self.z /= other
        
        return self
        
    def __str__(self):
        return "{}, {}, {}".format(self.x, self.y, self.z)
        
    def project(self, camera_position, camera_orientation, canvas_position): #project point onto 2d camera plane (this formula from wikipedia.org/wiki/3D_projection)
        cx, cy, cz = camera_position.x, camera_position.y, camera_position.z
        thx, thy, thz = camera_orientation[0], camera_orientation[1], camera_orientation[2]
        ex, ey, ez = canvas_position.x, canvas_position.y, canvas_position.z
        
        x = self.x - cx
        y = self.y - cy
        z = self.z - cz
        
        dx = cos(thy) * (sin(thz) * y + cos(thz) * x) - sin(thy) * z
        dy = sin(thx) * (cos(thy) * z + sin(thy) * (sin(thz) * y + cos(thz) * x)) + cos(thx) * (cos(thz) * y - sin(thz) * x)
        dz = cos(thx) * (cos(thy) * z + sin(thy) * (sin(thz) * y + cos(thz) * x)) - sin(thx) * (cos(thz) * y - sin(thz) * x)
        
        bx = (ez/dz) * dx + ex
        by = (ez/dz) * dy + ey
        
        return (bx, by)

def distance(a, b):
    return sqrt((b.x - a.x) ** 2 + (b.y - a.y) ** 2 + (b.z - a.z) ** 2)

class Star(vec3):
    def __init__(self, x, y, z):
        super().__init__(x,y,z)
        self.color = (255,255,255)
        self.size = 2
        
        self.distance = 0