import pygame, sys
from pygame import Surface, mouse
from player import Player
import obstacle
from alien import Alien, Extra
from random import choice, randint
from laser import Laser

class Game:
    
    def __init__(self):
        #mainMenu
        self.running=False
        
        
        #setup player
        player_sprite = Player((w/2,h),w,5)
        self.player = pygame.sprite.GroupSingle(player_sprite)
        
         #score and health
        self.lives=5
        img=pygame.image.load('../graphics/player.png').convert_alpha()
        self.live_surf=pygame.Surface((60,30))
        self.live_surf.blit(img,(0,0),((0,0),(60,30)))
        self.live_surf.set_colorkey((0,0,0))
        self.live_x_start_pos= w-(self.live_surf.get_size()[0]*(self.lives-1)+20)
        self.score=0
        self.font = pygame.font.Font('../font/Pixeled.ttf',20)
        
        #setup obstacles
        self.blocks = pygame.sprite.Group()
        self.shape = obstacle.shape
        self.block_size = 6
        
        self.obstacles_amount=4
        self.obstacles_x_pos=[num * (w / self.obstacles_amount) for num in range(self.obstacles_amount)]       
        self.create_multiple_obstacle(*self.obstacles_x_pos,x_start=w/15,y_start=480)
    
        #Alien setup
        self.aliens=pygame.sprite.Group()
        self.alien_lasers = pygame.sprite.Group()
        self.aliens_setup(rows=6,cols=12)
        self.alien_direction=1
        
        #Extra setup
        self.extra=pygame.sprite.GroupSingle()
        self.extra_spawn_time=randint(400,800)
        
        # Audio
        self.music = pygame.mixer.Sound('../audio/music.wav')
        self.music.set_volume(0.2)
        
        self.laser_sound = pygame.mixer.Sound('../audio/laser.wav')
        self.laser_sound.set_volume(0.5)
        self.explosion_sound = pygame.mixer.Sound('../audio/explosion.wav')
        self.explosion_sound.set_volume(0.3)

    def create_obstacle(self, x_start, y_start,offset_x):
        for row_index, row in enumerate(self.shape):
            for col_index, col in enumerate(row):
                if col=='x':
                   x = x_start+col_index*self.block_size+offset_x
                   y = y_start+row_index*self.block_size
                   block=obstacle.Block(self.block_size,(241,141,22),x,y)
                   self.blocks.add(block)
    
    def create_multiple_obstacle(self,*offset,x_start,y_start):
        for offset_x in offset:
            self.create_obstacle(x_start,y_start,offset_x)
    
    def aliens_setup(self,rows,cols,x_distance=60,y_distance=48,x_offset=70,y_offset=100):
        for row_index, row in enumerate(range(rows)):
            for col_index, col in enumerate(range(cols)):
                x= col_index * x_distance+x_offset
                y= row_index * y_distance+y_offset
                if row_index==0: alien_sprite=Alien('yellow',x,y)
                elif 1<= row_index <=2 : alien_sprite=Alien('green',x,y)
                else: alien_sprite=Alien('red',x,y)
                self.aliens.add(alien_sprite)
    
    def aliens_pos_cheker(self):
        all_aliens=self.aliens.sprites()
        for alien in all_aliens:
            if alien.rect.right>=w:
                self.alien_direction=-1
                self.aliens_move_down(2)
            elif alien.rect.left<=0:
                self.alien_direction=1
                self.aliens_move_down(2)
                
    def aliens_move_down(self,distance):
        if self.aliens:
            for alien in self.aliens.sprites():
                alien.rect.y+=distance
    
    def alien_shoot(self):
    	if self.aliens.sprites():
         random_alien = choice(self.aliens.sprites())
         laser_sprite = Laser(random_alien.rect.center,6,h)
         self.alien_lasers.add(laser_sprite)
                
                
    def extra_alien_timer(self):
        self.extra_spawn_time-=1
        if self.extra_spawn_time<=0:
            self.extra.add(Extra(choice(['right','left']),w))
            self.extra_spawn_time=randint(400,800)
   
    def collision_cheker(self):
       #player laser
        if self.player.sprite.lasers:
            for laser in self.player.sprite.lasers:
               #obstacle collision
               if pygame.sprite.spritecollide(laser,self.blocks,True):
                   laser.kill()
               #alien collision
               alien_hit = pygame.sprite.spritecollide(laser,self.aliens,True)
               
               if alien_hit:
                    for alien in alien_hit:
                        self.score += alien.value
                    laser.kill()
                    self.explosion_sound.play()
                #extra collision
               if pygame.sprite.spritecollide(laser,self.extra,True):
                   self.score+=500
                   laser.kill()
        #alien laser
        if self.alien_lasers:
            for laser in self.alien_lasers:
                #obstacle collision
               if pygame.sprite.spritecollide(laser,self.blocks,True):
                   laser.kill()
                #alien collision
               if pygame.sprite.spritecollide(laser,self.player,False):
                    laser.kill()
                    self.lives -= 1
                    if self.lives <= 0:
                        self.running=False
      
        #aliens
        if self.aliens:
            for alien in self.aliens:
                #obstacle collision
               pygame.sprite.spritecollide(alien,self.blocks,True)
                
                #alien collision
               if pygame.sprite.spritecollide(alien,self.player,True):
                   self.running=False
    
    def display_lives(self):
    	for live in range(self.lives - 1):
         x = self.live_x_start_pos + (live * (self.live_surf.get_size()[0] + 10))
         screen.blit(self.live_surf,(x,8))
       
     
    
    def display_score(self):
        score_surf = self.font.render(f'score : {self.score}',False,'white')
        score_rect = score_surf.get_rect(topleft = (10,-10))
        screen.blit(score_surf,score_rect)                     
    
    def victory_message(self):
        if not self.aliens.sprites():
            self.aliens_setup(rows=6,cols=12)
            self.alien_direction=1
            #victory_surf = self.font.render('You won',False,'white')
            #victory_rect = victory_surf.get_rect(center = (w / 2, h / 2))
            #screen.blit(victory_surf,victory_rect)
            
            #buttonImage = pygame.image.load('button.png').convert_alpha()
            #buttonImage=pygame.transform.scale(buttonImage,(32*4,16*4)).convert_alpha()
            #rect=buttonImage.get_rect(center=(w/2,h/2+210))
            #buttonImage.set_colorkey((255,255,255))
            
            #screen.blit(buttonImage,rect)
            #self.music.stop()
    def run(self):
        if self.running:
            self.player.update()
        
            self.alien_lasers.update()
            self.aliens_pos_cheker()
            self.extra_alien_timer()
            self.collision_cheker()
            self.aliens.update(self.alien_direction)
            self.extra.update()
            if self.player.sprite != None:
                self.player.sprite.lasers.draw(screen)
            self.player.draw(screen)
        
        
            self.blocks.draw(screen)
        
            self.aliens.draw(screen)
            self.alien_lasers.draw(screen)
            self.extra.draw(screen)
            self.display_lives()
            self.display_score()
            self.victory_message()
        
class CRT:
    def __init__(self):
        self.tv = pygame.image.load('../graphics/tv.png').convert_alpha()
        self.tv = pygame.transform.scale(self.tv,(w,h))

    def create_crt_lines(self):
        line_height = 3
        line_amount = int(h / line_height)
        for line in range(line_amount):
            y_pos = line * line_height
            pygame.draw.line(self.tv,'black',(0,y_pos),(w,y_pos),1)

    def draw(self):
        self.tv.set_alpha(randint(75,90))
        self.create_crt_lines()
        screen.blit(self.tv,(0,0))    

class Menu:
    def __init__(self):
        self.mainImage = pygame.image.load('menu.png').convert_alpha()
        self.buttonImage = pygame.image.load('button.png').convert_alpha()
        self.buttonImage=pygame.transform.scale(self.buttonImage,(32*4,16*4)).convert_alpha()
        self.buttonImage.set_colorkey((255,255,255))
        self.rect=self.buttonImage.get_rect(center=(w/2,h/2+210))
        self.game=Game()
    def initGame(self):
        self.game=Game()
            
    def draw(self, screen): 
        screen.blit(self.mainImage,(0,0))
        screen.blit(self.buttonImage,self.rect)
        
    def get_rect(self):
        return self.rect    
         
    def get_Game(self):
        return self.game
        
if __name__ == '__main__':                     
    
    pygame.init()

    w=1000
    h=600
    screen=pygame.display.set_mode((w,h))
    clock=pygame.time.Clock()
    menu=Menu()
    img = pygame.image.load('../graphics/bg.png')
    crt = CRT()
    running=True
    select= pygame.mixer.Sound('../audio/Select.wav')
    ALIENLASER = pygame.USEREVENT + 1
    pygame.time.set_timer(ALIENLASER,800)
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
               running=False
            if event.type == ALIENLASER and menu.game.running==True:
                menu.game.alien_shoot()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if menu.get_rect().collidepoint(mouse.get_pos()):
                     menu.initGame()
                     menu.game.music.play(loops = -1)
                     menu.game.running=True
                     select.play()
                     
        screen.blit(img,(0,0))    
        crt.draw()
        if menu.game.running:
            menu.game.run()
        else:
            menu.game.running=False
            menu.draw(screen)
            menu.game.music.stop()
          
        pygame.display.flip()
        clock.tick(80)
    pygame.quit()
    sys.exit()        
