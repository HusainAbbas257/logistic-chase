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
        moves = [0, 0, 0, 0]  # [up, down, left, right]

        def act(i, dvx=0, dvy=0):
            if dvx: self.vx += dvx
            if dvy: self.vy += dvy
            moves[i] = 1

        keymaps = {
            'wasd':  (pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d, pygame.K_SPACE),
            'arrow': (pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_RSHIFT)
        }

        if type_ in keymaps:
            ku,kd,kl,kr,kb = keymaps[type_]
            if keys[ku]: act(0, dvy=-self.speed)
            if keys[kd]: act(1, dvy= self.speed)
            if keys[kl]: act(2, dvx=-self.speed)
            if keys[kr]: act(3, dvx= self.speed)
            if kb and keys[kb]: self.vx*=0.925; self.vy*=0.925

        elif type_ == 'auto':
            e = entities[0]
            if e.y < self.y: act(0, dvy=-self.speed)
            if e.y > self.y: act(1, dvy= self.speed)
            if e.x < self.x: act(2, dvx=-self.speed)
            if e.x > self.x: act(3, dvx= self.speed)

        elif type_.endswith('.pkl'):
            e0,e1 = entities[0], entities[1]
            inp = [[e0.x,e0.y,e0.vx,e0.vy,e1.x,e1.y,e1.vx,e1.vy]]
            probs = [m.predict_proba(inp)[0][1] for m in self.models]
            for i,(p,vec) in enumerate(zip(
                probs,
                [(0,-self.speed),(0,self.speed),(-self.speed,0),(self.speed,0)]
            )):
                if p > self.threshold: act(i, dvx=vec[0], dvy=vec[1])
        else:
            raise ValueError(f'Unknown control type: {type_}')

        return moves
            
    def draw(self,screen:'pygame.Surface'):
        pygame.draw.circle(screen,self.color,(self.x,self.y),self.r)