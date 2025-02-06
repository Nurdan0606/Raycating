import pygame
from config import *
import math
from numba import jit

coord_map = []

for i in range(len(MAP)):
    for j in range(len(MAP[i])):
        if MAP[i][j] == "W":
            coord_map.append((i, j))

x, y = 400, 400
speed = 0.5
length = 800
count = 400
fov = math.radians(90)
angle = 0
alpha = math.radians(1)

@jit(nopython=True)
def line_shooter(x, y, length, count, fov, coord_map, angle):
    coords = []
    for ang in range(count):
        a = True
        for i in range(length):
            x2, y2 = int(x + i * math.cos(angle+ang*fov/count)), (y + i * math.sin(angle+ang*fov/count))
            if (x2//size , y2//size) in coord_map:
                coords.append((x2, y2))
                a = False
                break
        if a:
            coords.append((int(x + i * math.cos(angle+ang*fov/count)), (y + i * math.sin(angle+ang*fov/count))))
    return coords

all_sprites = pygame.sprite.Group()

dis = pygame.display.set_mode((W, H))
while True:
    dis.fill((0, 50, 150))
    for i in coord_map:
        pygame.draw.rect(dis, (200, 200, 200), (i[0]*size/10, i[1]*size/10, size/10, size/10))
    

    pygame.draw.circle(dis, (255, 0, 0), (x//10, y//10), 1)
    pygame.draw.rect(dis, (0, 100, 100), (0, H/2, W, H/2))

    for j, i in enumerate(line_shooter(x, y, length, count, fov, coord_map, angle)):
        pygame.draw.line(dis, (255, 0, 0),(x//10, y//10), (int(i[0])//10, int(i[1])//10))
        l = ((x-i[0])**2 + (y-i[1])**2)**0.5
        if l < 20:
            pygame.draw.rect(dis, (0, 255, 0), (W//count*j, 0, W//count, H))
        elif l >= 20 and l < length-5:
            pygame.draw.rect(dis, (0, 255-l/length*255, 0), (W//count*j, H/2 - H/2*length/l/30, W//count, H*length/l/30))

    all_sprites.update()
    all_sprites.draw(dis)


    key = pygame.key.get_pressed()
    if key[pygame.K_w]:
        y += speed*math.sin(angle+fov/2)
        x += speed*math.cos(angle+fov/2)
    if key[pygame.K_s]:
        y -= speed*math.sin(angle+fov/2)
        x -= speed*math.cos(angle+fov/2)
    if key[pygame.K_a]:
        y -= speed*math.sin(angle+fov/2+math.pi/2)
        x -= speed*math.cos(angle+fov/2+math.pi/2)
    if key[pygame.K_d]:
        y -= speed*math.sin(angle+fov/2-math.pi/2)
        x -= speed*math.cos(angle+fov/2-math.pi/2)
    
    if key[pygame.K_RIGHT]:
        angle += alpha
    if key[pygame.K_LEFT]:
        angle -= alpha

    
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()