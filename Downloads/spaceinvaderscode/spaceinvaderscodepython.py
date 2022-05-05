#spaceinvaderscode
from re import X
import pygame,sys
from player import Player
import obstacle
from alien import Alien,Extra
from random import choice,randint
from laser import Laser


class Game:
    def __init__(self): #where we load the sprites and initial stuff
        #Player Set up
        player_sprite = Player((screen_width/2,screen_height),screen_width,5)
        self.player = pygame.sprite.GroupSingle(player_sprite)
        
        #Obstacle Set up
        self.shape = obstacle.shape
        self.block_size = 6
        self.blocks = pygame.sprite.Group()
        self.obstacle_amount = 4
        self.obstacle_x_position = [num*(screen_width/self.obstacle_amount) for num in range(self.obstacle_amount)]
        self.create_multiple_obstacles(*self.obstacle_x_position,x_start = screen_width/15,y_start = 480)

        #Alien_setup
        self.aliens = pygame.sprite.Group()
        self.alien_setup(rows=6,cols=8)
        self.alien_direction = 1
        self.alien_lasers = pygame.sprite.Group()
        
        #extra alien setup
        self.extra = pygame.sprite.GroupSingle()
        self.extra_spawn_time = randint(40,80)

        #health, lives and sore setup
        self.lives = 3
        self.live_surf = pygame.image.load('C:/Users/franc/Downloads/spaceinvaderscode/Space-invaders-main/graphics/player.png').convert_alpha()
        self.live_x_start_pos = screen_width - (self.live_surf.get_size()[0]*2 + 20)
        self.score = 0
        self.font = pygame.font.Font('C:/Users/franc/Downloads/spaceinvaderscode/Space-invaders-main/font/Pixeled.ttf',20)

        #Audio
        music = pygame.mixer.Sound('C:/Users/franc/Downloads/spaceinvaderscode/Space-invaders-main/audio/music.wav')
        music.set_volume(0.15)
        music.play(loops=-1)



    def create_obstacle(self,x_start,y_start,offset_x):
        for row_index,row in enumerate(self.shape):
            for col_index,col in enumerate(row):
                if col == 'x':
                    x = x_start + col_index*self.block_size+ offset_x
                    y = y_start + row_index*self.block_size
                    block = obstacle.Block(self.block_size,(241,79,80),x,y)
                    self.blocks.add(block)

    def create_multiple_obstacles(self,*offset,x_start,y_start):
        for offset_x in offset:
            self.create_obstacle(x_start,y_start,offset_x)

    def alien_setup(self,rows,cols,x_distance=60,y_distance=48,x_offset=70,y_offset=100):
        for row_index,row in enumerate(range(rows)):
            for col_index,col in enumerate(range(cols)):
                x = col_index* x_distance + x_offset
                y = row_index*y_distance + y_offset
                if row_index == 0: alien_sprite = Alien('yellow',x,y)
                elif 1<= row_index <= 2: alien_sprite = Alien('green',x,y)
                else: alien_sprite = Alien('red',x,y)
                self.aliens.add(alien_sprite)

    def alien_position_checker(self):
        all_aliens = self.aliens.sprites()
        for alien in all_aliens:
            if alien.rect.right >= screen_width:
                self.alien_direction = -1
                self.alien_move_down(2)
            elif alien.rect.left <= 0:
                self.alien_direction = 1
                self.alien_move_down(2) 


    def alien_move_down(self,distance):
        if self.aliens:
            for aliens in self.aliens.sprites():
                aliens.rect.y += distance

    def alien_shoot(self):
        if self.aliens.sprites():
            random_alien = choice(self.aliens.sprites())
            laser_sprite = Laser(random_alien.rect.center,6,screen_height)
            self.alien_lasers.add(laser_sprite)
            laser_sound = pygame.mixer.Sound('C:/Users/franc/Downloads/spaceinvaderscode/Space-invaders-main/audio/laser.wav')
            laser_sound.set_volume(0.2)
            laser_sound.play()

    def extra_alien_timer(self):
        self.extra_spawn_time -= 1
        if self.extra_spawn_time <= 0:
                self.extra.add(Extra(choice(['right','left']),screen_width))
                self.extra_spawn_time = randint(400,800)

    def collision_checks(self):

        #player lasers
        if self.player.sprite.lasers:
            for laser in self.player.sprite.lasers:
                if pygame.sprite.spritecollide(laser,self.blocks,True):
                    laser.kill()

                #alien collisions
                aliens_hit = pygame.sprite.spritecollide(laser,self.aliens,True)
                if aliens_hit:
                    for alien in aliens_hit:
                        self.score += alien.value
                    laser.kill()
                    alien_hit_sound = pygame.mixer.Sound('C:/Users/franc/Downloads/spaceinvaderscode/Space-invaders-main/audio/explosion.wav')
                    alien_hit_sound.set_volume(0.15)
                    alien_hit_sound.play()


                #extra collisions
                if pygame.sprite.spritecollide(laser,self.extra,True):
                    laser.kill()
                    self.score += 500
                    alien_hit_sound = pygame.mixer.Sound('C:/Users/franc/Downloads/spaceinvaderscode/Space-invaders-main/audio/explosion.wav')
                    alien_hit_sound.set_volume(0.15)
                    alien_hit_sound.play()

        if self.alien_lasers:
            for laser in self.alien_lasers:
                if pygame.sprite.spritecollide(laser,self.player,False):
                    laser.kill()
                    self.lives -= 1
                    if self.lives <= 0:
                        pygame.quit()
                        sys.exit()

                if pygame.sprite.spritecollide(laser,self.blocks,True):
                    laser.kill()

        if self.aliens:
            for alien in self.aliens:
                pygame.sprite.spritecollide(alien,self.blocks,True)

                if pygame.sprite.spritecollide(alien,self.player,False):
                    pygame.quit()
                    sys.exit()

                    
    def display_lives(self):
        for live in range(self.lives - 1):
            x = self.live_x_start_pos + (live*(self.live_surf.get_size()[0] + 10))
            screen.blit(self.live_surf,(x,8))

    def display_score(self):
        score_text = self.font.render(f'score: {self.score}',False,'white')
        score_rect = score_text.get_rect(topleft = (10,-10))
        screen.blit(score_text,score_rect)



    
    def run(self): #the main part of game
        self.player.update()
        self.player.sprite.lasers.draw(screen)
        self.player.draw(screen)
        self.blocks.draw(screen)
        self.aliens.draw(screen)
        self.aliens.update(self.alien_direction)
        self.alien_position_checker()
        self.alien_lasers.draw(screen)
        self.alien_lasers.update()
        self.extra_alien_timer()
        self.extra.draw(screen)
        self.extra.update()
        self.collision_checks()
        self.display_lives()
        self.display_score()
        
        
class CRT:
    def __init__(self):
        self.tv = pygame.image.load('C:/Users/franc/Downloads/spaceinvaderscode/Space-invaders-main/graphics/tv.png')
        self.tv = pygame.transform.scale(self.tv,(screen_width,screen_height))

    def create_crt_lines(self):
        line_height = 3
        line_amount = int(screen_height/line_height)
        for line in range(line_amount):
            y_pos = line*line_height
            pygame.draw.line(self.tv,'black',(0,y_pos),(screen_width,y_pos),1)

    def draw(self):
        self.tv.set_alpha(randint(75,90))
        screen.blit(self.tv,(0,0))
        self.create_crt_lines()

if __name__ == '__main__':
    pygame.init()
    screen_width = 600
    screen_height = 600
    screen = pygame.display.set_mode((screen_width,screen_height))
    clock = pygame.time.Clock()
    game= Game()
    crt = CRT()


    ALIENLASER = pygame.USEREVENT + 1
    pygame.time.set_timer(ALIENLASER,800)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == ALIENLASER:
                game.alien_shoot()

        screen.fill((30,30,30))
        game.run()
        crt.draw()

        pygame.display.flip()
        clock.tick(60)