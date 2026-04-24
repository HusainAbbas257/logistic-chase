import pygame
import numpy as np
pygame.init()
from src.entity import Entity
screen=pygame.display.set_mode((1200,720),)
font=pygame.font.SysFont('arial',32)
width,height=screen.get_width(),screen.get_height()
clock=pygame.time.Clock()


def mainloop(enemy_type='auto'):
    # a note for myself first one is ai(enemy) and second one is human
    entities:list[Entity]=[Entity((100,100),10,control='wasd'),Entity((500,700),20,color="#09ff00",control=enemy_type)]
    data=[]
    running=True
    moves=[]
    while running:
        screen.fill((0,0,0))
        # events 
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                running=False
        keys=pygame.key.get_pressed()
        # updating:
        for entity in entities:
            moves.append(entity.keyboard_input(keys,entities))
            entity.update(keys,entities,clock.get_fps())
            for other in entities:
                if(entity.check_collision(other)):
                    running=endScreen()
                    entity.reset()
                    other.reset()
            entity.draw(screen)
       
        # drawing
        screen.blit(font.render(f'fps:{int(clock.get_fps())}',True,(100,100,100)),(10,10))
        data.append(frame_data(entities,keys,moves[-1]))
        pygame.display.flip()
        clock.tick(60)
    return data
def endScreen():
    while True:
        screen.fill((0,0,0))
        # events 
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                return False
        keys=pygame.key.get_pressed()
        if keys[pygame.K_q]:return False
        if keys[pygame.K_r]:return True
        # drawing
        screen.blit(font.render(f'fps:{int(clock.get_fps())}',True,(100,100,100)),(10,10))
        screen.blit(font.render(f'Game Over',True,(100,100,100)),(550,360))
        screen.blit(font.render(f'press R for replay',True,(100,100,100)),(550,400))
        screen.blit(font.render(f'press q for quit',True,(100,100,100)),(550,440))
        pygame.display.flip()
        clock.tick(60)

def frame_data(entities:list[Entity],keys:pygame.key.ScancodeWrapper,bot_moves:list[int]):
    return np.array([entities[0].x,entities[0].y,entities[0].vx,entities[0].vy,entities[1].x,entities[1].y,entities[1].vx,entities[1].vy,int(keys[pygame.K_w]),int(keys[pygame.K_a]),int(keys[pygame.K_s]),int(keys[pygame.K_d]),bot_moves[0],bot_moves[1],bot_moves[2],bot_moves[3]],dtype=np.int16)
if __name__=='__main__':
    mainloop()