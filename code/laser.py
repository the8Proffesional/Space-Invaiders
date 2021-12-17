import pygame

class Laser(pygame.sprite.Sprite):
    def __init__(self,pos,speed,screen_height):
        super().__init__()
        self.image=pygame.Surface((4,20))
        img=pygame.image.load('../graphics/laser.png')
        self.image.blit(img,(0,0))
        self.rect=self.image.get_rect(center=pos)
        self.speed=speed
        self.height_y_constraint=screen_height
    
    def destry(self):
        if self.rect.y <= -50 or self.rect.y >= self.height_y_constraint+50:
            self.kill
    
        
    def update(self):
        self.rect.y += self.speed
        self.destry()
            
        
        
    