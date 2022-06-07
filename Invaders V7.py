from cgi import test
from os import kill, remove
import time
from time import sleep
import pygame
from pygame import mixer
from pygame.locals import *
import random
import math
import buttonfunction

pygame.init


#set display
screen_height = 960
screen_width = 720

rows = 5 
coll = 6

screens = pygame.display.set_mode((128, 128))
clocks = pygame.time.Clock()

counter, text = 10, '10'.rjust(3)
pygame.time.set_timer(pygame.USEREVENT, 1000)


#game over function
game_over = 0

#refresh rate
clock = pygame.time.Clock()
fps = 59
fps2 = 500

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Invaders')
anti_spam = 1000
global last_alien_shot
last_alien_shot = pygame.time.get_ticks()

#health bar colour
red = (255, 0, 0,)
green = (0, 255, 0)

#images
skydrop = pygame.image.load("Assets\Space.png").convert()
skydrop_width = skydrop.get_width()

#help screen
helpscreen = pygame.image.load("Assets\HelpMenu.png").convert_alpha()

def show_help():
    screen.blit(helpscreen,(90,125))

#splashscreen
splashsc = pygame.image.load("Assets\SplashScreen.png")

def draw_splash():
    screen.blit(splashsc, (0,250))

#buttons
startbutton = pygame.image.load("Assets\StartButton.png").convert_alpha()
quitbutton = pygame.image.load("Assets\QuitButton.png").convert_alpha()
helpbutton = pygame.image.load("Assets\HelpButton.png").convert_alpha()
backbutton = pygame.image.load("Assets\BackButton.png").convert_alpha()
testbutton = pygame.image.load("Assets\Quit.png").convert_alpha()

#win screen
winbutton = pygame.image.load("Assets\YouWin.png").convert_alpha()

def draw_win():
    screen.blit(winbutton, (0, 0))


class Button():
    def __init__(self, x, y, image, scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int (height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)
        self.clicked = False

    def draw(self):
        action = False
        #click pos
        pos = pygame.mouse.get_pos()

        #click button
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True

            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False

        screen.blit(self.image,(self.rect.x, self.rect.y))

        return action
#BUTTONS
start_button = buttonfunction.Button(90, 800, startbutton, 0.25)
start_button2 = buttonfunction.Button(90, 700, startbutton, 0.25)
exit_button = buttonfunction.Button(400, 800, quitbutton, 0.25)
help_button = buttonfunction.Button(550, 10, helpbutton, 0.15)
back_button = buttonfunction.Button(50, 10, backbutton, 0.15)
test_button = buttonfunction.Button(90, 800, testbutton, 0.25)

#def testing():
    #screen

#keyboard inputs

#background load
def draw_background():
    screen.blit(skydrop, (0, 0))

#spaceship
class Spaceship(pygame.sprite.Sprite):
    def __init__(self, x, y, health):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("Assets\Ship.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.health_start = health
        self.health_remaining = health
        self.last_shot = pygame.time.get_ticks()

    def update(self):
        speed = 8

        bulletlimiter = 300

        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= speed
        if key[pygame.K_RIGHT] and self.rect.right < screen_width:
            self.rect.x += speed

        time_now = pygame.time.get_ticks()
        #shooting
        if key[pygame.K_SPACE] and time_now - self.last_shot > bulletlimiter:
            bullet = Bullets(self.rect.centerx, self.rect.top)
            bullet_group.add(bullet)
            self.last_shot = time_now

#bullets
class Bullets(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("Assets\Bullet.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

    def update(self):
        self.rect.y -= 7
        if pygame.sprite.spritecollide(self, alien_group, True):
            self.kill()



class Alien(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("Assets\Alien.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.move_counter = 0
        self.movement = 3

    def update(self):
        self.rect.x += self.movement
        self.move_counter += abs(self.movement)
        if abs(self.move_counter) > 100:
            self.movement *= -1
            self.move_counter *= -1

class AlienBullets(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("Assets\Bullet.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

    def update(self):
        self.rect.y += 2
        if self.rect.top > screen_height:
            self.kill()

#def collision_checks(self):

    #if self.sprite.bullets:
    #    for bullet in self.player.sprite.bullets:
     #       for bullets in self.player.sprite.bullets:
      #          if pygame.spritecollide(bullet,self.aliens,True):
      #              bullet.kill()

                           
spaceship_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
alien_group = pygame.sprite.Group()
alien_bull_group = pygame.sprite.Group()

def create_aliens():
    for row in range(rows):
        for item in range(coll):
            aliens = Alien(100 + item * 100, 100 + row * 70)
            alien_group.add(aliens)

create_aliens()

spaceship = Spaceship(int(screen_width / 2), screen_height - 100, 3)
spaceship_group.add(spaceship)

#movement


#button functions
def help():
    running = True
    while running:
        screen.fill((0,0,0))
        draw_background()
        show_help()
        back_button.draw(screen)
        for event in pygame.event.get():
            if back_button.draw(screen):
                pygame.display.set_caption("Invaders")
                running = False
        pygame.display.update()

def game2():
    running = True
    create_aliens()
    while running:
        clock.tick(fps)
        screen.fill((0,0,0))
        draw_background()
        spaceship.update()
        spaceship_group.draw(screen)
        bullet_group.update()
        alien_group.update()
        bullet_group.draw(screen)
        back_button.draw(screen)
        alien_group.draw(screen)
        alien_bull_group.update()
        alien_bull_group.draw(screen)
        last_alien_shot = pygame.time.get_ticks()
        time_now = pygame.time.get_ticks()
        if len(alien_group) == 0:
            create_aliens()
        for event in pygame.event.get():
            if back_button.draw(screen):
                running = False
                alien_group.kill
        pygame.display.update()
    


def game():
    running = True
    create_aliens()
    while running:
        clock.tick(fps)
        screen.fill((0,0,0))
        draw_background()
        spaceship.update()
        spaceship_group.draw(screen)
        bullet_group.update()
        alien_group.update()
        bullet_group.draw(screen)
        back_button.draw(screen)
        alien_group.draw(screen)
        alien_bull_group.update()
        alien_bull_group.draw(screen)
        if len(alien_group) == 0:
            draw_win()
            time.sleep(1)
            print("You Won")
            draw_win()
            print("A")
            time.sleep(2)
            main()
            clock.tick(fps2)
            time.sleep(1)
            create_aliens()
            print("ready")
            running = False
        last_alien_shot = pygame.time.get_ticks()
        time_now = pygame.time.get_ticks()
        for event in pygame.event.get():
            if back_button.draw(screen):
                
                running = False
        pygame.display.update()
    


def main():    
    running = True
    while running:

        clock.tick(fps)
        
        #background
        draw_background()

    
        last_alien_shot = pygame.time.get_ticks()
        time_now = pygame.time.get_ticks()
        if time_now - last_alien_shot > anti_spam and len(alien_bull_group) < 5 and len(alien_group) > 0:
            attacking_alien = random.choice(alien_group.sprites())
            alien_bullet = AlienBullets(attacking_alien.rect.centerx, attacking_alien.rect.bottom)
            alien_bull_group.add(alien_bullet)
            last_alien_shot = time_now
        
    
        #splashscreen
        draw_splash()

        #display buttons
        if start_button.draw(screen):
                print("Start")
                game()
        
        if start_button2.draw(screen):
                game2()

        if exit_button.draw(screen):
            print("Quit")
            running = False
        if help_button.draw(screen):
            pygame.display.set_caption("Help")
            help()
        

        #event handlers
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        pygame.display.update()

    pygame.quit
    
main()