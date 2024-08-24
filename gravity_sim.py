import pygame
import math
import random




n = int(input("enter no of planets"))
pygame.init()


screen = pygame.display.set_mode((800, 600))
black = (0, 0, 0)
running = True


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

bodies = initialize(bodies,n)

history = []
for i in range(n):
    history.append([])



def update(ls,mode=0):
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

        ##trace stuff
        if mode == 0:
            if len(history[i]) >5000:
                history[i].pop(0)    
            history[i].append((x,y))
    return ls

def track(bodies):
    xmean = 0
    ymean = 0
    for i in bodies:
        x,y,_,_,_,_ = i
        xmean += x
        ymean += y
    xmean /= len(bodies)
    ymean /= len(bodies)

    xmean -= 400
    ymean -=300
    for i in range(len(bodies)):
        x,y,i1,i2,i3,i4 = bodies[i]
        x -= xmean
        y -= ymean
        bodies[i] = x,y,i1,i2,i3,i4
    return bodies


def trace(ls):

    for i in range(len(history)):
        for j in range(len(history[i])-1):
            _,_,_,_,_,c = bodies[i]
            pygame.draw.aaline(screen,c,history[i][j+1],history[i][j])
        
def draw(ls):

    for i in ls:
        x,y,m,vx,vy,c = i
        pygame.draw.circle(screen, c, (int(x), int(y)), m)

def gravity_well(bodies,mouse_pos):
    x,y = mouse_pos
    print(x,y)
    well = [x,y,9999999999999,0,0,(0,0,0)]
    ls = bodies.copy()
    ls.append(well)
    ls = update(ls,1)
    return ls[:-1]
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    mouse_buttons = pygame.mouse.get_pressed()
    mouse_pos = pygame.mouse.get_pos()

    if mouse_buttons[0]:  # Left mouse button is held down
        if not gravity_well_active:
            bodies = gravity_well(bodies, mouse_pos)
            gravity_well_active = True
    else:  # Mouse button is not pressed
        gravity_well_active = False

    
    screen.fill(black)
    bodies = track(bodies)

    bodies = update(bodies)
    trace(bodies)
    
    draw(bodies)
    
    
    pygame.display.flip()

pygame.quit()
