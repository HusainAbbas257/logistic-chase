import pygame
import math
import joblib
import random
width,height=1200,720
class Entity:
    def __init__(self,size:tuple[int,int],radius:int,color="#dd0f0f",control:str='',type_='c'):
        self.x,self.y=random.randint(radius,size[0]-radius),random.randint(radius,size[1]-radius)
        if(type_ in ['r','c']):
            self.type=type_
        else:
            self.type='c'
        self.vx,self.vy=0,0
        self.r=radius
        self.color=color
        self.speed=5
        self.control=control
        self.model=None
        if self.control.endswith('.pkl'):
            self.model=joblib.load(control)
        self.threshold=0.4
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
    def reset(self,size:tuple[int,int]):
        self.x,self.y=random.randint(self.r,size[0]-self.r),random.randint(self.r,size[1]-self.r)
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
            if self.type=='c':
                e = entities[0] #runner
                if e.y < self.y: act(0, dvy=-self.speed)
                if e.y > self.y: act(1, dvy= self.speed)
                if e.x < self.x: act(2, dvx=-self.speed)
                if e.x > self.x: act(3, dvx= self.speed)
            else:
                e = entities[1]
                dx = self.x - e.x
                dy = self.y - e.y

                # if enemy is far or in corner move towards center else run bro
                margin=self.r*3
                if abs(dx) + abs(dy) > 700 or  self.x < self.r + margin or self.x > width - self.r - margin or    self.y < self.r + margin or self.y > height - self.r - margin:

                    cx, cy =600+random.randint(-100,100), 360+random.randint(-100,100) # a little randomness brings joy
                    tx, ty = cx - self.x, cy - self.y
                else:
                    tx, ty = dx, dy

                # small randomness brings joy again
                tx += random.uniform(-3, 3)
                ty += random.uniform(-3, 3)

                if abs(tx) > abs(ty):
                    if tx > 0 and self.x < width - self.r: act(3, dvx=self.speed)
                    elif tx < 0 and self.x > self.r:       act(2, dvx=-self.speed)
                else:
                    if ty > 0 and self.y < height - self.r: act(1, dvy=self.speed)
                    elif ty < 0 and self.y > self.r:        act(0, dvy=-self.speed)
        elif type_.endswith('.pkl'):
            e0,e1 = entities[0], entities[1]
            inp = [[e0.x,e0.y,e0.vx,e0.vy,e1.x,e1.y,e1.vx,e1.vy,
                    e1.x-e0.x,e1.y-e0.y,e1.vx-e0.vx,e1.vy-e0.vy]]

            probs = [p[0][1] for p in self.model.predict_proba(inp)]  # correct extraction

            best_i = max(range(4), key=lambda i: probs[i])  # choose best
            vecs = [(0,-self.speed),(0,self.speed),(-self.speed,0),(self.speed,0)]
            act(best_i, dvx=vecs[best_i][0], dvy=vecs[best_i][1])
        else:
            raise ValueError(f'Unknown control type: {type_}')

        return moves
            
    def draw(self,screen:'pygame.Surface'):
        pygame.draw.circle(screen,self.color,(self.x,self.y),self.r)