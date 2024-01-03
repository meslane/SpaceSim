import pygame
from math import *
import random
import time

import starmap

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
        s = starmap.Star(random.randint(0,255),random.randint(0,255),random.randint(0,255))
        s.color = (random.randint(100,255),random.randint(100,255),random.randint(100,255))
        map.stars.append(s)
    
    #main loop
    locked = False
    fps = 0
    while True:
        startloop = time.time()
    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    locked = False
                    pygame.mouse.set_visible(True)
                    pygame.event.set_grab(False)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if not locked:
                    locked = True
                    pygame.mouse.set_visible(False)
                    pygame.event.set_grab(True)
            
        keys = pygame.key.get_pressed()
        
        #lateral + forward motion
        motion = [0,0] #x,z
        move_mag = 0.25
        
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
        fps_text = font.render("{}".format(fps), False, (255, 255, 255))
        
        map.map.blit(ppos, (20,10))
        map.map.blit(pang, (20,20))
        map.map.blit(fps_text, (20,30))
        
        pygame.draw.line(map.map, (255, 255, 255), (w_screen//2 - 5, h_screen//2), (w_screen//2 + 5, h_screen//2), 1)
        pygame.draw.line(map.map, (255, 255, 255), (w_screen//2, h_screen//2 - 5), (w_screen//2, h_screen//2 + 5), 1)
    
        window.blit(pygame.transform.scale(map.map, window.get_rect().size), (0, 0))
        pygame.display.flip()
        
        fps = 1/(time.time() - startloop + 0.01)

if __name__ == '__main__':
    main()