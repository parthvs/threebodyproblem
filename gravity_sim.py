import pygame
import math
import random
pygame.init()

screen = pygame.display.set_mode((800, 600))
black = (0, 0, 0)
running = True

'''
x1, y1, m1 ,vx1, vy1 = 100, 400, 1, 0, 0

x2, y2, m2 ,vx2, vy2= 400, 100, 1,0 ,0

x3, y3, m3 ,vx3, vy3= 700, 400, 1,0 ,0



centre = [400,300, 5, 0, 0, (0,0,0)]
body1 = [x1, y1, m1 ,vx1, vy1, (66, 135, 245)]
body2 =[x2, y2, m2 ,vx2, vy2,(245, 66, 87)]
body3 =[x3, y3, m3 ,vx3, vy3,(245, 191, 66)]

bodies = [centre,body1,body2,body3]'''


def initialize(ls,n):
    for i in range(n):
        x = random.randint(50,750)
        y = random.randint(50,550)
        m = 10
        vx = 0
        vy = 0
        color = (random.randint(100,255),random.randint(100,255),random.randint(100,255))
        temp = [x, y, m, vx, vy, color]
        ls.append(temp)
    return ls
G = 0.5

bodies= []
bodies = initialize(bodies,5)
def update(ls):
    force= []
    for i in range(len(ls)):
        force.append((0,0))
    for i in range(len(ls)):
        for j in range(i+1,len(ls)):

            x1,y1,m1,vx1,vy1,c= ls[i]
            x2,y2,m2,vx2,vy2,c= ls[j]
            
            r = math.hypot(x1-x2,y1-y2)
            if r > m1+m2:
                
                f = (G * m1 * m2)/(r**2)
                theta = math.atan2(y2-y1,x2-x1)
                tfx = f * math.cos(theta)
                tfy = f * math.sin(theta)
                
                fx,fy = force[i] 
                fx += tfx
                fy += tfy
                
                force[i] =  (fx,fy)

                fx,fy = force[j] 
                fx += -tfx
                fy += -tfy
                
                force[j] =  (fx,fy)
    for i in range(len(ls)):
        fx, fy = force[i]
        x, y, m, vx, vy, c = ls[i]

        vx += fx/m
        vy += fy/m
        x  += vx
        y  += vy
        ls[i] = x, y, m, vx, vy, c 
    return ls

        
def draw(ls):

    for i in ls:
        x,y,m,vx,vy,c = i
        pygame.draw.circle(screen, c, (int(x), int(y)), m)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(black)
    bodies = update(bodies)
    draw(bodies)

    
 
    
    pygame.display.flip()

pygame.quit()
