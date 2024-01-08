import pygame
from math import *
import random
import time

import starmap
import geometry
import worldgen

w_screen = 320 * 2
h_screen = 180 * 2

def main():
    #setup
    pygame.init()
    pygame.display.set_caption("Space Simulator")
    
    font = pygame.font.SysFont("Consolas", 10)
    
    window = pygame.display.set_mode([w_screen,h_screen], pygame.RESIZABLE)
    
    map = starmap.Starmap((w_screen, h_screen))
    
    random.seed(0)
    
    for i in range(255):
        s = worldgen.generate_star(-127,127)
        #s.color = (random.randint(100,255),random.randint(100,255),random.randint(100,255))
        s.name = "S-{}".format(i)
        map.objects.append(s)
    
    #map.objects.append(geometry.line(map.objects[0], map.objects[1], t=2))
    #map.objects.append(geometry.line(map.objects[1], map.objects[2], t=2))
    
    origin = worldgen.Star(0,0,0)
    origin.color = (255,237,227)
    origin.size = 1
    origin.name = "Homeworld"
    
    map.objects.append(origin)
    
    #main loop
    locked = False
    fps = 0
    tick = 0
    while True:
        startloop = time.time()
    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    locked = False
                    pygame.mouse.set_visible(True)
                    pygame.event.set_grab(False)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if not locked:
                    locked = True
                    pygame.mouse.set_visible(False)
                    pygame.event.set_grab(True)
            elif event.type == pygame.MOUSEWHEEL:
                if event.y > 0 and map.canvas_position.z > 0:
                    map.canvas_position.z -= 50
                elif event.y < 0:
                    map.canvas_position.z += 50 #zoom
                    
                print(map.canvas_position.z)
            
        keys = pygame.key.get_pressed()
        
        #lateral + forward motion
        motion = [0,0] #x,z
        move_mag = 0.25
        
        if keys[pygame.K_LSHIFT]:
            move_mag = 0.5
        
        if keys[pygame.K_w]:
            motion[1] = move_mag
        if keys[pygame.K_s]:
            motion[1] = -move_mag
        if keys[pygame.K_a]:
            motion[0] = -move_mag
        if keys[pygame.K_d]:
            motion[0] = move_mag
        #vertical motion
        if keys[pygame.K_r]:
            map.camera_position.y -= move_mag
        if keys[pygame.K_f]:
            map.camera_position.y += move_mag
        
        map.camera_position.x += motion[1] * sin(map.camera_orientation[1])
        map.camera_position.y -= motion[1] * sin(map.camera_orientation[0])
        map.camera_position.z += motion[1] * cos(map.camera_orientation[1])
        map.camera_position.x += motion[0] * sin(map.camera_orientation[1] + radians(90))
        #map.camera_position.y -= motion[0] * sin(map.camera_orientation[1] + radians(90))
        map.camera_position.z += motion[0] * cos(map.camera_orientation[1] + radians(90))   
        
        max_distance = 200
        
        #position/rotation limits
        if map.camera_position.x > max_distance:
            map.camera_position.x = max_distance
        elif map.camera_position.x < -max_distance:
            map.camera_position.x = -max_distance
            
        if map.camera_position.y > max_distance:
            map.camera_position.y = max_distance
        elif map.camera_position.y < -max_distance:
            map.camera_position.y = -max_distance
            
        if map.camera_position.z > max_distance:
            map.camera_position.z = max_distance
        elif map.camera_position.z < -max_distance:
            map.camera_position.z = -max_distance
        
        if map.camera_orientation[0] > pi/2:
            map.camera_orientation[0] = pi/2
        elif map.camera_orientation[0] < -pi/2:
            map.camera_orientation[0] = -pi/2
        
        if locked:
            pygame.mouse.set_pos(w_screen//2,h_screen//2)
            
            m = pygame.mouse.get_rel()
            
            if m[0] != 0 and abs(m[0]) < 300: #if the mouse moved, move camera
                map.camera_orientation[1] += radians(m[0]/10)
            if m[1] != 0 and abs(m[1]) < 300:
                map.camera_orientation[0] -= radians(m[1]/10)
        
        map.draw_starmap()
        
        ppos = font.render("{}".format(map.camera_position), False, (255, 255, 255))
        pang = font.render("{}".format(map.camera_orientation), False, (255, 255, 255))
        pang_rect = font.render("{}".format(geometry.spherical_to_rect(1, map.camera_orientation[0], map.camera_orientation[1])), 
                                False, 
                                (255, 255, 255))
        fps_text = font.render("{}".format(fps), False, (255, 255, 255))
        
        map.map.blit(ppos, (20,10))
        map.map.blit(pang, (20,20))
        map.map.blit(pang_rect, (20,30))
        map.map.blit(fps_text, (20,40))
        
        pygame.draw.line(map.map, (255, 255, 255), (w_screen//2 - 5, h_screen//2), (w_screen//2 + 5, h_screen//2), 1)
        pygame.draw.line(map.map, (255, 255, 255), (w_screen//2, h_screen//2 - 5), (w_screen//2, h_screen//2 + 5), 1)
    
        #ellipse
        #test_ellipse = geometry.ellipse(50 * sin(radians(tick % 180)), 50, tick%360, (w_screen//2,h_screen//2), width=2)
        #test_ellipse.draw(map.map)
        
        test_ellipse = geometry.ellipse_3D(geometry.vec3(20,10,10), geometry.vec3(10,20,10), geometry.vec3(10,10,10))
        test_ellipse.draw(map.map, map.camera_position, map.camera_orientation, map.canvas_position,
                            xoffset = w_screen//2, yoffset = h_screen//2)
    
        #this goes last
        window.blit(pygame.transform.scale(map.map, window.get_rect().size), (0, 0))
        pygame.display.flip()
        
        fps = 1/(time.time() - startloop + 0.01)
        tick += 1

if __name__ == '__main__':
    main()