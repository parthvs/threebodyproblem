import pygame
import math
import random
import os

def clear_console():
    if os.name == 'nt':  # 'nt' indicates Windows
        os.system('cls')
    else:  # For other operating systems like Linux or macOS
        os.system('clear')

clear_console()

print("THREE BODY PROBLEM SIM 2D")
a = "=="
a = a*50

print("\n",a,"\n\n")

print("Instructions:\n1.You can press T to toggle trace on or off\n2.You can press S to toggle sparkle effect on or off\n")
n =3

black = (0, 0, 0)
running = True

trace_active = -1
gravity_well_active = False
sparkle_active = -1
graph_active = -1 

def initialize(ls,n):
    for i in range(n):
        print(f"body {i}")
        x = random.randint(10,700)
        y = random.randint(10,600)
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
vel_his = []

for i in range(n):
    history.append([])
    vel_his.append([])




pygame.init()


screen = pygame.display.set_mode((800, 600))

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
        if len(history[i]) >100000:
            history[i].pop(0)    
        history[i].append((x,y))
        
        if len(vel_his[i]) > 1000000:
            vel_his[i].pop(0)
        vel_his[i].append((vx,vy))
        print(vx,vy)
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
            pygame.draw.line(screen,c,history[i][j+1],history[i][j],1)
        
def draw(ls):

    for i in ls:
        x,y,m,vx,vy,c = i
        if sparkle_active == 1:
            draw_sparkles((int(x),int(y)), c)
        else:
            pygame.draw.circle(screen, c, (int(x), int(y)), m)

def draw_sparkles(centre,color):
    radius_max = 10
    for i in range(20):
        radius = random.randint(1,radius_max)
        theta = random.uniform(0,math.pi*2)
        x,y = centre
        x1 = x  + radius * math.cos(theta)
        x2 = x  - radius * math.cos(theta)
        y1 = y  + radius * math.sin(theta)
        y2 = y - radius * math.sin(theta)
        pygame.draw.line(screen, color, (x1,y1),(x2,y2),1)

def graph(history):

    for i in range(len(history)):
        for j in range(len(history[i])-1):
            scale = 250
            x1,y1 = history[i][j+1]
            x1,y1 = (x1 * scale) + 400, (y1 * scale) + 300
            x2,y2 = history[i][j]
            x2,y2 = (x2 * scale) + 400, (y2 * scale) + 300
            if i == 0:
                c = (255,140,0)
                #pygame.draw.aaline(screen,c,(x1,y1),(x2,y2))
            if i== 1:
                c = (255,0,0)
            if i == 2:
                c = (255,255,0)
            pygame.draw.aaline(screen,c,(x1,y1),(x2,y2))

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_t:
                trace_active *= -1 
            if event.key == pygame.K_s:
                sparkle_active *= -1
            if event.key == pygame.K_g:
                graph_active *= -1


    screen.fill(black)

    bodies = update(bodies) 
    if graph_active == -1:
        bodies = track(bodies)
        if(trace_active ==1):
            trace(bodies)
        
        draw(bodies)
    if graph_active == 1:
        graph(vel_his)
        
        
    pygame.display.flip()

pygame.quit()
