import pygame
from laser import Laser

class Player(pygame.sprite.Sprite):

    def __init__(self,pos,constraint,speed):
        super().__init__()
        self.image = pygame.image.load('C:/Users/franc/Downloads/spaceinvaderscode/Space-invaders-main/graphics/player.png').convert_alpha()
        self.rect = self.image.get_rect(midbottom=pos)
        self.speed = speed
        self.max_x_constraint = constraint
        self.ready = True
        self.laser_time = 0
        self.laser_cooldown = 600

        self.lasers = pygame.sprite.Group()

    def get_input(self):
        key = pygame.key.get_pressed()

        if key[pygame.K_RIGHT]:
            self.rect.x += self.speed
        elif key[pygame.K_LEFT]:
            self.rect.x -= self.speed

        if key[pygame.K_SPACE] and self.ready:
            self.shoot_laser()
            self.ready = False
            self.laser_time = pygame.time.get_ticks()
            laser_sound = pygame.mixer.Sound('C:/Users/franc/Downloads/spaceinvaderscode/Space-invaders-main/audio/laser.wav')
            laser_sound.set_volume(0.2)
            laser_sound.play()

        
    def recharge(self):
        if not self.ready:
            current_time = pygame.time.get_ticks()
            if current_time - self.laser_time >= self.laser_cooldown:
                self.ready = True


    def constraint(self):
        if self.rect.left <= 0:
            self.rect.left = 0
        elif self.rect.right >= self.max_x_constraint:
            self.rect.right = self.max_x_constraint

    def shoot_laser(self):
        self.lasers.add(Laser(self.rect.center,-8,self.rect.bottom))
        


    def update(self):
        self.constraint()
        self.get_input()
        self.recharge()
        self.lasers.update()
        
