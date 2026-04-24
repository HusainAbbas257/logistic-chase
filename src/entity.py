import pygame
import math

class Entity:
    def __init__(self,pos:tuple[int,int],radius:int,color="#dd0f0f",control:str=None):
        self.x,self.y=pos
        self.original=pos
        self.vx,self.vy=0,0
        self.r=radius
        self.color=color
        self.speed=5
        self.control=control
    def update(self,keys:pygame.key.ScancodeWrapper,fps:float=60):
        if(self.control!=None):
            self.keyboard_input(keys)
        fps=max(fps,0.01)
        self.x+=self.vx*(1/fps)
        self.y+=self.vy*(1/fps)
    def check_collision(self,other:'Entity'):
        return (math.dist((self.x,self.y),(other.x,other.y))<=1.05*(self.r+other.r)) if other!=self else False
    def reset(self):
        self.x,self.y=self.original
        self.vx,self.vy=0,0
        self.speed=5
    def keyboard_input(self,keys:pygame.key.ScancodeWrapper):
        type_=self.control
        if type_==None:
            type_='wasd'
        
        if type_=='wasd':
            if keys[pygame.K_w]: self.vy -= self.speed
            if keys[pygame.K_s]: self.vy += self.speed
            if keys[pygame.K_a]: self.vx -= self.speed
            if keys[pygame.K_d]: self.vx += self.speed
        elif(type_=='arrow'):
            if keys[pygame.K_UP]: self.vy -= self.speed
            if keys[pygame.K_DOWN]: self.vy += self.speed
            if keys[pygame.K_LEFT]: self.vx -= self.speed
            if keys[pygame.K_RIGHT]: self.vx += self.speed
        else:
            raise ValueError('the type speified for controls is not found:',type_)
            
    def draw(self,screen:'pygame.Surface'):
        pygame.draw.circle(screen,self.color,(self.x,self.y),self.r)