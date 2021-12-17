import pygame
from pygame.sprite import Group
from  laser import Laser



class Player(pygame.sprite.Sprite):
    def __init__(self, pos, constraint, speed):
        super().__init__()
        self.frameIndex=0
        self.img=pygame.image.load('../graphics/player.png').convert_alpha()
        self.image = pygame.Surface((60,30))
        self.image.blit(self.img,(0,0),((0,0),(60,30)))
        self.image.set_colorkey((0,0,0))
        self.rect = self.image.get_rect(midbottom = pos)
        self.speed=speed
        self.max_x_constraint=constraint
        self.ready=True
        self.laser_time=0
        self.laser_coldown=600
        
        self.lasers=pygame.sprite.Group()
        self.laser_sound = pygame.mixer.Sound('../audio/laser.wav')
        self.laser_sound.set_volume(0.5)
        
    def get_input(self):
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
            
        elif keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
            
        if keys[pygame.K_SPACE] and self.ready:
            self.shoot_laser()
            self.laser_time=pygame.time.get_ticks()
            self.ready=False
            self.laser_sound.play()


    def recharge(self):
        if not self.ready:
            current_time=pygame.time.get_ticks()
            if current_time - self.laser_time >= self.laser_coldown:
                self.ready=True
        
    def animate(self):
        if self.frameIndex < 1:
            self.frameIndex+=1
        else:
            self.frameIndex=0
        self.image = pygame.Surface((60,30))
        self.image.blit(self.img,(0,0),((0,30*self.frameIndex),(60,30)))
        self.image.set_colorkey((0,0,0))
               
    def shoot_laser(self):
        self.lasers.add(Laser(self.rect.center,-8,self.rect.bottom))

    def constraint(self):
        if self.rect.left <= 0 :
            self.rect.left = 0
        if self.rect.right >= self.max_x_constraint :
            self.rect.right = self.max_x_constraint
            
    def update(self):
        self.animate()
        self.get_input()
        self.constraint()
        self.recharge()
        self.lasers.update()
        
   
     
