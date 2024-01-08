import pygame
import random

import geometry
import starmap

#Keplerian orbital elements (https://en.wikipedia.org/wiki/Orbital_elements)
class Keplerian:
    def __init__(self):
        self.e = 0 #eccentricity 
        self.a = 0 #semi-major axis
        
        self.i = 0 #inclination
        self.omega = 0 #longitude of ascending node
        
        self.w = 0 #argument of periapsis
        self.theta = 0 #true anomaly

class Star(geometry.vec3):
    def __init__(self, x, y, z):
        super().__init__(x,y,z)
        self.star_class = 'G'
        self.color = (255,255,255)
        self.size = 2
        
        self.distance = 0
        
        self.name = "star"

class Planet:
    def __init__(self):
        pass

def generate_star(min_pos, max_pos):
    s = Star(random.uniform(min_pos, max_pos),
                    random.uniform(min_pos, max_pos),
                    random.uniform(min_pos, max_pos))
    
    color_range = 10
    
    sequence = random.uniform(0, 40)
    color_var = (random.randint(-color_range,color_range),
                random.randint(-color_range,color_range),
                random.randint(-color_range,color_range))
    
    if sequence <= 0.003:
        s.star_class = 'O'
        s.color = (146,181,255)
        s.size = random.uniform(6.6, 10)
    elif sequence <= 0.12:
        s.star_class = 'B'
        s.color = (162,192,255)
        s.size = random.uniform(1.8, 6.6)
    elif sequence <= 0.73:
        s.star_class = 'A'
        s.color = (213,224,255)
        s.size = random.uniform(1.4, 1.8)
    elif sequence <= 3.73:
        s.star_class = 'F'
        s.color = (249, 245, 255)
        s.size = random.uniform(1.15, 1.4)
    elif sequence <= 11.33:
        s.star_class = 'G'
        s.color = (255,237,227)
        s.size = random.uniform(0.95, 1.15)
    elif sequence <= 23.33:
        s.star_class = 'K'
        s.color = (255,218,181)
        s.size = random.uniform(0.7, 0.95)
    else:
        s.star_class = 'M'
        s.color = (255,181,208)
        s.size = random.uniform(0.4, 0.7)
    
    star_color = [s.color[0] + color_var[0],
                s.color[1] + color_var[1],
                s.color[2] + color_var[2]]
                
    for i, color in enumerate(star_color):
        if color > 255:
            star_color[i] = 255
    
    s.color = (star_color[0], star_color[1], star_color[2])

    s.size = round(s.size, 2)
    
    return s