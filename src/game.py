import pygame
pygame.init()
from src.entity import Entity
screen=pygame.display.set_mode((1200,720),)
font=pygame.font.SysFont('arial',32)
width,height=screen.get_width(),screen.get_height()
clock=pygame.time.Clock()


entities:Entity=[Entity((100,100),10)]
def mainloop():
    running=True
    while running:
        screen.fill((0,0,0))
        # events 
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                running=False
        # updating:
        for entity in entities:
            entity.update()
            entity.draw(screen)
        
        # drawing
        screen.blit(font.render(f'fps:{int(clock.get_fps())}',True,(100,100,100)),(10,10))
            
        pygame.display.flip()
        clock.tick(60)
        


if __name__=='__main__':
    mainloop()