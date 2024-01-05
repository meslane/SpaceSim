import pygame
from math import *

def distance(a, b): #find distance between 2 points
    return sqrt((b.x - a.x) ** 2 + (b.y - a.y) ** 2 + (b.z - a.z) ** 2)

def midpoint(a, b): #find midpoint of line
    return vec3((a.x + b.x)/2, (a.y + b.y)/2, (a.z + b.z)/2)

def mag(a): #magnitude of vec3
    return sqrt(a.x ** 2 + a.y ** 2 + a.z ** 2)

def norm(a): #norm of vector
    return a / mag(a)

def crossProduct(a, b): #find the cross product between two points
    return vec3(a.y * b.z - a.z * b.y,
            a.z * b.x - a.x * b.z,
            a.x * b.y - a.y * b.x)

def dotProduct(a, b): #find the dot product between two points
    return (a.x * b.x) + (a.y * b.y) + (a.z * b.z)

def directionVector(a, b): #find the direction vector from point a -> b
    return vec3(b.x - a.x, b.y - a.y, b.z - a.z)

def distance_to_line(l, p): #get distance between line l and point p
    x1 = l.p1
    x2 = l.p2
    x0 = p

    d = mag(crossProduct(x2 - x1, x1 - x0))/mag(x2 - x1)
    
    #print(d)
    return d
    
def spherical_to_rect(rho, theta, phi): #convert spherical coords to x,y,z
    x = rho * sin(phi) * cos(theta)
    y = rho * sin(phi) * sin(theta)
    z = rho * cos(phi)
    
    return vec3(x,y,z)
    
class vec3:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        
    def __add__(self, other): #addition/subtraction operators
        return vec3(self.x + other.x, self.y + other.y, self.z + other.z)
    
    def __sub__(self, other):
        return vec3(self.x - other.x, self.y - other.y, self.z - other.z)
        
    def __truediv__(self, other): #overload operators for scalar multiplication/division
        return vec3(self.x / other, self.y / other, self.z / other)
        
    def __mul__(self, other):
        return vec3(self.x * other, self.y * other, self.z * other)
        
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

class line:
    def __init__(self, p1, p2, **kwargs):
        self.p1 = p1
        self.p2 = p2
        self.color = (255,255,255)
        self.thickness = kwargs.get('t', 1)
        
        self.distance = 0
        
    def draw(self, surface, camera_position, camera_orientation, canvas_position, **kwargs):
        xoffset = kwargs.get('xoffset', 0)
        yoffset = kwargs.get('yoffset', 0)
    
        pr1 = self.p1.project(camera_position, 
                                camera_orientation, 
                                canvas_position)
        pr2 = self.p2.project(camera_position, 
                                camera_orientation, 
                                canvas_position)
        pygame.draw.line(surface, self.color, (pr1[0] + xoffset, pr1[1] + yoffset), 
                                                (pr2[0] + xoffset, pr2[1] + yoffset), width=self.thickness)
        
    def draw_literal(self, surface): #project to screen based on x/y only
        pygame.draw.line(surface, self.color, (self.p1.x, self.p1.y), (self.p2.x, self.p2.y), 1)