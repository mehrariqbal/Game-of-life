from select import select
from tkinter import CENTER
import pygame
import random
import math
from pygame import gfxdraw

# intialize the pygame 
pygame.init()

# creating screen
screen = pygame.display.set_mode((860,660))

# Game title
pygame.display.set_caption("life")

# background
background = pygame.image.load('background.png')

class box(pygame.sprite.Sprite):
    def __init__(self,x,y):
        self.p = 0
        self.dead = [0,0,0]
        self.alive = [100,200,100]
        self.border = pygame.Rect(x,y,10,10)
        gfxdraw.rectangle(screen,self.border,[0,0,0])
        self.body = pygame.Rect(x+1,y+1,8,8)
        self.situation = self.dead
        gfxdraw.box(screen,self.body,self.situation)
        self.clicked = False

    def update(self,event_list):
        for event in event_list:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.border.collidepoint(event.pos):
                   self.clicked = not self.clicked
        if self.clicked:
           self.situation = self.alive
           gfxdraw.box(screen,self.body,self.situation)
        else:
            self.situation = self.dead
            gfxdraw.box(screen,self.body,self.situation)

    def neighbour(self,grp,a):
        self.p = 0
        if a == 0:
            l = [grp[a+1],grp[a+66],grp[a+67]]
        elif a > 0 and a < 65:
            l = [grp[a+1],grp[a-1],grp[a+65],grp[a+66],grp[a+67]]
        elif a == 65:
            l = [grp[a-1],grp[a+65],grp[a+66]]
        elif a > 65 and (a+67)%66 == 0 and a< 5675:
            l = [grp[a-67],grp[a-66],grp[a-1],grp[a+65],grp[a+66]]
        elif a > 0 and (a+66)%66 == 0 and a+65 < 5675:
            l = [grp[a-66],grp[a-65],grp[a+1],grp[a+66],grp[a+67]]
        elif a == 5610:
            l = [grp[a-66],grp[a-65],grp[a+1]]
        elif a > 5610 and a < 5675:
            l = [grp[a-67],grp[a-66],grp[a-65],grp[a+1],grp[a-1]]
        elif a == 5675:
            l = [grp[a-66],grp[a-67],grp[a-1]]
        else:
            l = [grp[a-1],grp[a+1],grp[a-66],grp[a+66],grp[a-67],grp[a+67],grp[a-65],grp[a+65]]
        
        for i in l:
            if i.clicked:
                self.p += 1

    def life(self):
        if self.clicked:
            if self.p < 2 or self.p >3:
                self.clicked= False
                
        elif self.clicked == False:
            if self.p == 3:
                self.clicked = True

        if self.clicked:
            self.situation = self.alive
            gfxdraw.box(screen,self.body,self.situation)
        else:
            self.situation = self.dead
            gfxdraw.box(screen,self.body,self.situation)
        
grp = []
for i in range(0,screen.get_width(),10):
        for j in range(0,screen.get_height(),10):
            grp.append(box(i,j))  

def reset(grp):
    for j in grp:
        j.clicked = False

#score
count_cells = 0
txtx= 740
txty= 18
def count(x,y,z):
    font = pygame.font.Font('freesansbold.ttf',z)
    n = font.render("count: " + str(count_cells),True,(100,100,255))
    screen.blit(n,(x,y))

r = False
running = True
while running:

    #screen filling with black color
    screen.fill((0,0,0))

    event_list = pygame.event.get()

    for event in event_list:
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                r = not r
            if event.key == pygame.K_r:
                reset(grp)
    if r:
        for j in grp:
            j.life()

    for j in grp:
        j.update(event_list)
        j.neighbour(grp,grp.index(j))
        if j.clicked:
            count_cells += 1
    count(txtx,txty,20)
    count_cells = 0
    pygame.display.update()

    