import pygame

class Player(pygame.sprite.Sprite):

    def __init__(self,pos):
        super().__init__()
        self.image = pygame.image.load('C:/Users/franc/Downloads/spaceinvaderscode/Space-invaders-main/graphics/player.png').convert_alpha()
        self.rect = self.image.get_rect(midbottom=pos)
        self.speed = 5

    def get_input(self):
        key = pygame.key.get_pressed()

        if key[pygame.K_RIGHT]:
            self.rect.x += self.speed
        elif key[pygame.K_LEFT]:
            self.rect.x -= self.speed

    def update(self):
        self.get_input()
        
