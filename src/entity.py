import pygame

class Entity:
    def __init__(self,pos:tuple[int,int],radius:int,color="#dd0f0f"):
        self.x,self.y=pos
        self.vx,self.vy=0,0
        self.r=radius
        self.color=color
    def update(self,fps:float=60):
        self.x+=self.vx*(1/fps)
        self.y+=self.vy*(1/fps)
    def draw(self,screen:'pygame.Surface'):
        pygame.draw.circle(screen,self.color,(self.x,self.y),self.r)