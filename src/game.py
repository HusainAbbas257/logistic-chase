import pygame
pygame.init()
from src.entity import Entity
screen=pygame.display.set_mode((1200,720),)
font=pygame.font.SysFont('arial',32)
width,height=screen.get_width(),screen.get_height()
clock=pygame.time.Clock()


entities:Entity=[Entity((100,100),10,control='wasd'),Entity((200,100),20,color="#09ff00",control='arrow')]
def mainloop():
    running=True
    while running:
        screen.fill((0,0,0))
        # events 
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                running=False
        keys=pygame.key.get_pressed()
        # updating:
        for entity in entities:
            entity.update(keys,clock.get_fps())
            for other in entities:
                if(entity.check_collision(other)):
                    running=endScreen()
                    entity.reset()
                    other.reset()
            entity.draw(screen)
       
        # drawing
        screen.blit(font.render(f'fps:{int(clock.get_fps())}',True,(100,100,100)),(10,10))
            
        pygame.display.flip()
        clock.tick(60)
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


if __name__=='__main__':
    mainloop()