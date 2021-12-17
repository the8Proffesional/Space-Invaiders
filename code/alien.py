import pygame

class Alien(pygame.sprite.Sprite):
    
    def __init__(self,color,x,y):
        super().__init__()
        file_path='../graphics/'+color+'.png'
        self.indexFrame=0
        self.img=pygame.image.load(file_path).convert_alpha()
        self.image=pygame.Surface((40,32))
        self.image.blit(self.img,(0,0),((0,0),(40,32)))
        self.image.set_colorkey((0,0,0))
        self.rect=self.image.get_rect(topleft=(x,y))
        if color=='red': self.value=100
        elif color=='green': self.value=200
        else: self.value=300
        
    def animate(self):
        if self.indexFrame<2:
            self.indexFrame+=0.15
        else:
            self.indexFrame=0
        self.image=pygame.Surface((40,32))
        self.image.blit(self.img,(0,0),((0,int(self.indexFrame)*32),(40,32)))
        self.image.set_colorkey((0,0,0))
    def update(self, direction):
        self.animate()
        self.rect.x+=direction


class Extra(pygame.sprite.Sprite):
    def __init__(self,side,w):
        super().__init__()
        self.image=pygame.image.load('../graphics/extra.png')
        if side == 'right':
            x=w+50
            self.speed=-3
        else:
            x=-50
            self.speed=3
        self.rect=self.image.get_rect(topleft=(x,80))
    def update(self):
        self.rect.x += self.speed