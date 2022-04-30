import pygame

class Alien(pygame.sprite.Sprite):
    def __init__(self,color,x,y):
        super().__init__()
        file_path = 'C:/Users/franc/Downloads/spaceinvaderscode/Space-invaders-main/graphics/'+color+'.png'
        self.image = pygame.image.load(file_path).convert_alpha()
        self.rect = self.image.get_rect(topleft = (x,y))

    def update(self,direction):
        self.rect.x += direction
