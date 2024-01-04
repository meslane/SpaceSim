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

class Starmap:
    def __init__(self, size):
        self.size = size
        self.map = pygame.Surface(size)
        self.objects = []
        
        #camera params
        self.camera_position = vec3(0,0,0)
        self.camera_orientation = [0,0,0]
        self.canvas_position = vec3(0,0,1000)
        
        #axis lines
        compass_offset = 30
        self.compass_origin = vec3(compass_offset, self.size[1] - compass_offset, 0)
        
        self.x_axis = line(self.compass_origin, self.compass_origin)
        self.y_axis = line(self.compass_origin, self.compass_origin)
        self.z_axis = line(self.compass_origin, self.compass_origin)
        
        '''
        self.x_axis.color = (255,0,0)
        self.y_axis.color = (0,255,0)
        self.z_axis.color = (0,0,255)
        '''
   
        print(self.x_axis.color)
        
    def draw_starmap(self):
        self.map.fill((0,0,0))
        
        #get camera vector
        v_camera = spherical_to_rect(1, self.camera_orientation[0], self.camera_orientation[1])
        
        #painter's algorithm
        for obj in self.objects:
            if type(obj) is Star:
                obj.distance = distance(obj, self.camera_position)
            elif type(obj) is line:
                #obj.distance = distance(midpoint(obj.p1, obj.p2), self.camera_position)
                obj.distance = distance_to_line(obj, self.camera_position)
        
        self.objects.sort(key = lambda x: x.distance, reverse = True) #python's sort method is faster than inorder insertion
        
        for obj in self.objects:
            if type(obj) is Star:
                obj_dir = directionVector(self.camera_position, obj)
            
                if dotProduct(obj_dir, v_camera) > 0: #only draw if in front of player
                    size = obj.size * 400 / obj.distance
                    
                    if size < 2:
                        size = 2
                
                    screen_pos = obj.project(self.camera_position, 
                                                self.camera_orientation, 
                                                self.canvas_position)
                
                    screen_pos = (screen_pos[0] + self.size[0]//2, screen_pos[1] + self.size[1]//2)
                
                    pygame.draw.circle(self.map, 
                                    obj.color, 
                                    screen_pos,
                                    size)
            elif type(obj) is line:
                dir = directionVector(self.camera_position, midpoint(obj.p1, obj.p2))
            
                if dotProduct(dir, v_camera) > 0:
                    obj.draw(self.map, self.camera_position, 
                                    self.camera_orientation, 
                                    self.canvas_position,
                                    xoffset = self.size[0]//2,
                                    yoffset = self.size[1]//2)
                                    
        #draw coords
        phi = self.camera_orientation[1]
        theta = self.camera_orientation[0]
        ref_size = 20
        
        self.x_axis.p2 = self.compass_origin + vec3(1 * sin(phi), sin(theta) * cos(phi), 0) * ref_size
        self.y_axis.p2 = self.compass_origin + vec3(0, -1 * cos(theta), 0) * ref_size
        self.z_axis.p2 = self.compass_origin + vec3(1 * cos(phi), sin(theta) * -sin(phi), 0) * ref_size
        
        self.x_axis.draw_literal(self.map)
        self.y_axis.draw_literal(self.map)
        self.z_axis.draw_literal(self.map)
        
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

class Star(vec3):
    def __init__(self, x, y, z):
        super().__init__(x,y,z)
        self.color = (255,255,255)
        self.size = 2
        
        self.distance = 0