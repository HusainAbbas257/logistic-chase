import pygame
import math
import joblib

class Entity:
    def __init__(self,pos:tuple[int,int],radius:int,color="#dd0f0f",control:str=''):
        self.x,self.y=pos
        self.original=pos
        self.vx,self.vy=0,0
        self.r=radius
        self.color=color
        self.speed=5
        self.control=control
        self.models=None
        if self.control.endswith('.pkl'):
            self.models=joblib.load(control)
    def update(self,keys:pygame.key.ScancodeWrapper,entities:list['Entity'],fps:float=60,width=1200,height=720):
        if(self.control!=''):
            self.keyboard_input(keys,entities)
        fps=max(fps,0.01)
        self.vx*=0.995
        self.vy*=0.995

        self.x+=self.vx*(1/fps)
        self.y+=self.vy*(1/fps)
        self.x%=width
        self.y%=height
    def check_collision(self,other:'Entity'):
        return (math.dist((self.x,self.y),(other.x,other.y))<=1.05*(self.r+other.r)) if other!=self else False
    def reset(self):
        self.x,self.y=self.original
        self.vx,self.vy=0,0
        self.speed=5
    def keyboard_input(self,keys:pygame.key.ScancodeWrapper,entities:list['Entity']):
        type_=self.control
        if type_=='':
            type_='wasd'
        
        if type_=='wasd':
            if keys[pygame.K_w]: self.vy -= self.speed
            if keys[pygame.K_s]: self.vy += self.speed
            if keys[pygame.K_a]: self.vx -= self.speed
            if keys[pygame.K_d]: self.vx += self.speed
            if keys[pygame.K_SPACE]:
                self.vx *=0.925
                self.vy*=0.925
        elif(type_=='arrow'):
            if keys[pygame.K_UP]: self.vy -= self.speed
            if keys[pygame.K_DOWN]: self.vy += self.speed
            if keys[pygame.K_LEFT]: self.vx -= self.speed
            if keys[pygame.K_RIGHT]: self.vx += self.speed

            if keys[pygame.K_RSHIFT]:
                self.vx *=0.925
                self.vy*=0.925
        elif(type_.endswith('.pkl')):
            pr=[model.predict([[entities[0].x,entities[0].y,entities[0].vx,entities[0].vy,entities[1].x,entities[1].y,entities[1].vx,entities[1].vy,int(keys[pygame.K_w]),int(keys[pygame.K_a]),int(keys[pygame.K_s]),int(keys[pygame.K_d])]]) for model in self.models]
            if pr[0]: self.vy -= self.speed
            if pr[1]: self.vy += self.speed
            if pr[2]: self.vx -= self.speed
            if pr[3]: self.vx += self.speed
        else:
            raise ValueError('the type speified for controls is not found:',type_)
            
    def draw(self,screen:'pygame.Surface'):
        pygame.draw.circle(screen,self.color,(self.x,self.y),self.r)