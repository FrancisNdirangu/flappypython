import pygame


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

    def get_input(self):
        key = pygame.key.get_pressed()

        if key[pygame.K_RIGHT]:
            self.rect.x += self.speed
        elif key[pygame.K_LEFT]:
            self.rect.x -= self.speed

        if key[pygame.K_SPACE]:
            self.shoot_laser()
            self.ready = False
            self.laser_time = pygame.time.get_ticks()

        
    


    def constraint(self):
        if self.rect.left <= 0:
            self.rect.left = 0
        elif self.rect.right >= self.max_x_constraint:
            self.rect.right = self.max_x_constraint

    def shoot_laser(self):
        print('shoot laser')


    def update(self):
        self.constraint()
        self.get_input()
        
