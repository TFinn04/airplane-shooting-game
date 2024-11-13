from enemy import Enemy
from constants import *

import random
def new_formation():
    x=random.randint(1,3)
    if x==1:
        return formation1()
    if x==2:
        return formation2()
    if x==3:
        return formation3()

def formation1():
    formation = []
    x=random.randint(screen_width // 4,(screen_width // 4) * 3)
    y=random.randint(2,4)
    pos=0
    
    layers=random.randint(0,3)
    for i in range(y):
        for layer in range(layers):
            if pos==0:
                formation.append(Enemy(x,-(enemy_height*(i+1)//1.75)-layer*enemy_height,1))
                
                
            else:
                
                formation.append(Enemy(x+pos,-((enemy_height*(i+1))//1.75)-layer*enemy_height,1))
                formation.append(Enemy(x-pos,-((enemy_height*(i+1))//1.75)-layer*enemy_height,1))
        pos+=enemy_width
            

    return formation

def formation2():
    formation = []
    x=0
    y=random.randint(0,100)
    layers=random.randint(0,3)
        
    for i in range (random.randint(1,5)):
        for layer in range(layers):
            formation.append(Enemy(x-(enemy_width*i),y-(enemy_height*i)//1.75-layer*enemy_height,2))
            formation.append(Enemy(screen_width+enemy_width*i,y-(enemy_height*i)//1.75-layer*enemy_height,-2))
    return formation  
def formation3():
    formation = []
    x=0
    
    layers=random.randint(100,400)
        
    for i in range (10):
        for layer in range(0,layers,enemy_height*2):
            formation.append(Enemy(-enemy_width*i,layer,3))
            formation.append(Enemy(screen_width+enemy_width*i,layer+enemy_height,-3))
    return formation   