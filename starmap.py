import pygame
from math import *

import geometry

class Starmap:
    def __init__(self, size):
        self.size = size
        self.map = pygame.Surface(size)
        self.objects = []
        
        #camera params
        self.camera_position = geometry.vec3(0,0,0)
        self.camera_orientation = [0,0,0]
        self.canvas_position = geometry.vec3(0,0,1000)
        
        #axis lines
        compass_offset = 30
        self.compass_origin = geometry.vec3(compass_offset, self.size[1] - compass_offset, 0)
        
        self.x_axis = geometry.line(self.compass_origin, self.compass_origin)
        self.y_axis = geometry.line(self.compass_origin, self.compass_origin)
        self.z_axis = geometry.line(self.compass_origin, self.compass_origin)
        
        '''
        self.x_axis.color = (255,0,0)
        self.y_axis.color = (0,255,0)
        self.z_axis.color = (0,0,255)
        '''
        
        #text
        self.font = pygame.font.SysFont("Consolas", 11)
        self.name_draw_distace = 170
        self.info_draw_distace = 50
   
        print(self.x_axis.color)
        
    def draw_starmap(self):
        self.map.fill((0,0,0))
        
        #get camera vector
        v_camera = geometry.spherical_to_rect(1, self.camera_orientation[0], self.camera_orientation[1])
        
        #painter's algorithm
        for obj in self.objects:
            if type(obj) is Star:
                obj.distance = geometry.distance(obj, self.camera_position)
            elif type(obj) is geometry.line:
                #obj.distance = distance(midpoint(obj.p1, obj.p2), self.camera_position)
                obj.distance = geometry.distance_to_line(obj, self.camera_position)
        
        self.objects.sort(key = lambda x: x.distance, reverse = True) #python's sort method is faster than inorder insertion
        
        for obj in self.objects:
            if type(obj) is Star:
                obj_dir = geometry.directionVector(self.camera_position, obj)
            
                if geometry.dotProduct(obj_dir, v_camera) > 0: #only draw if in front of player
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
                                    
                    if obj.distance < self.name_draw_distace: #draw name if close enough
                        name_text = self.font.render("{}".format(obj.name), False, (255, 255, 255))
                        text_size = self.font.size("{}".format(obj.name))
                        self.map.blit(name_text, (screen_pos[0]  - text_size[0]//2, 
                                                    screen_pos[1] - size - text_size[1]//2 - 10))
                    
                    if obj.distance < self.info_draw_distace: #draw info if close enough
                        string = "Class {}, R = {} sols".format(obj.star_class, obj.size)
                        info_text = self.font.render(string, False, (255, 255, 255))
                        text_size = self.font.size(string)
                        self.map.blit(info_text, (screen_pos[0]  - text_size[0]//2, 
                                                    screen_pos[1] + size + text_size[1]//2 + 5))
                        
            elif type(obj) is geometry.line:
                dir = geometry.directionVector(self.camera_position, geometry.midpoint(obj.p1, obj.p2))
            
                if geometry.dotProduct(dir, v_camera) > 0:
                    obj.draw(self.map, self.camera_position, 
                                    self.camera_orientation, 
                                    self.canvas_position,
                                    xoffset = self.size[0]//2,
                                    yoffset = self.size[1]//2)
                                    
        #draw coords
        phi = self.camera_orientation[1]
        theta = self.camera_orientation[0]
        ref_size = 20
        
        self.x_axis.p2 = self.compass_origin + geometry.vec3(1 * sin(phi), sin(theta) * cos(phi), 0) * ref_size
        self.y_axis.p2 = self.compass_origin + geometry.vec3(0, -1 * cos(theta), 0) * ref_size
        self.z_axis.p2 = self.compass_origin + geometry.vec3(1 * cos(phi), sin(theta) * -sin(phi), 0) * ref_size
        
        self.x_axis.draw_literal(self.map)
        self.y_axis.draw_literal(self.map)
        self.z_axis.draw_literal(self.map)

class Star(geometry.vec3):
    def __init__(self, x, y, z):
        super().__init__(x,y,z)
        self.star_class = 'G'
        self.color = (255,255,255)
        self.size = 2
        
        self.distance = 0
        
        self.name = "star"