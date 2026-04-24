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
        self.threshold=0.3
    def update(self,keys:pygame.key.ScancodeWrapper,entities:list['Entity'],fps:float=60,width=1200,height=720):
        fps=max(fps,0.01)
        self.vx*=0.995
        self.vy*=0.995

        self.x+=self.vx*(1/fps)
        self.y+=self.vy*(1/fps)
        if(self.x<self.r):
            self.x=self.r
            self.vx*=-0.5
        if(self.x>width-self.r):
            self.x=width-self.r
            self.vx*=-0.5
        if(self.y<self.r):
            self.y=self.r
            self.vy*=-0.5
        if(self.y>height-self.r):
            self.y=height-self.r
            self.vy*=-0.5
        

    def check_collision(self,other:'Entity'):
        return (math.dist((self.x,self.y),(other.x,other.y))<=1.05*(self.r+other.r)) if other!=self else False
    def reset(self):
        self.x,self.y=self.original
        self.vx,self.vy=0,0
        self.speed=5
    
    # refactoring this up
    def keyboard_input(self, keys, entities):
        type_ = self.control or 'wasd'
        moves = [0, 0, 0, 0]

        def apply(k_up, k_down, k_left, k_right, k_brake):
            if keys[k_up]:   self.vy -= self.speed; moves[0]=1
            if keys[k_down]: self.vy += self.speed; moves[1]=1
            if keys[k_left]: self.vx -= self.speed; moves[2]=1
            if keys[k_right]:self.vx += self.speed; moves[3]=1
            if k_brake and keys[k_brake]:
                self.vx *= 0.925; self.vy *= 0.925

        if type_ == 'wasd':
            apply(pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d, pygame.K_SPACE)

        elif type_ == 'arrow':
            apply(pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_RSHIFT)

        elif type_ == 'auto':
            e = entities[0]
            if e.x < self.x: self.vx -= self.speed; moves[2]=1
            if e.x > self.x: self.vx += self.speed; moves[3]=1
            if e.y < self.y: self.vy -= self.speed; moves[0]=1
            if e.y > self.y: self.vy += self.speed; moves[1]=1

        elif type_.endswith('.pkl'):
            e0, e1 = entities[0], entities[1]
            inp = [[e0.x,e0.y,e0.vx,e0.vy,e1.x,e1.y,e1.vx,e1.vy,
                    int(keys[pygame.K_w]),int(keys[pygame.K_a]),
                    int(keys[pygame.K_s]),int(keys[pygame.K_d])]]

            probs = [m.predict_proba(inp)[0][1] for m in self.models]

            if probs[0] > self.threshold: self.vy += self.speed; moves[0]=1
            if probs[1] > self.threshold: self.vy -= self.speed; moves[1]=1
            if probs[2] > self.threshold: self.vx += self.speed; moves[2]=1
            if probs[3] > self.threshold: self.vx -= self.speed; moves[3]=1
        else:
            raise ValueError(f'Unknown control type: {type_}')

        return moves
            
    def draw(self,screen:'pygame.Surface'):
        pygame.draw.circle(screen,self.color,(self.x,self.y),self.r)