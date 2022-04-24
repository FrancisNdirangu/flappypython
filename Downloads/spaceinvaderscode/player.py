import pygame


class Player(pygame.sprite.Sprite):

    def __init__(self,pos,constraint,speed):
        super().__init__()
        self.image = pygame.image.load('C:/Users/franc/Downloads/spaceinvaderscode/Space-invaders-main/graphics/player.png').convert_alpha()
        self.rect = self.image.get_rect(midbottom=pos)
        self.speed = speed
        self.max_x_constraint = constraint

    def get_input(self):
        key = pygame.key.get_pressed()

        if key[pygame.K_RIGHT]:
            self.rect.x += self.speed
        elif key[pygame.K_LEFT]:
            self.rect.x -= self.speed

    def constraint(self):
        if self.rect.left <= 0:
            self.rect.left = 0
        elif self.rect.right >= self.max_x_constraint:
            self.rect.right = self.max_x_constraint
    def update(self):
        self.constraint()
        self.get_input()
        
