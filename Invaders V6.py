from cgi import test
import pygame
from pygame import mixer
from pygame.locals import *
import random
import math
import buttonfunction

pygame.init

#refresh rate
clock = pygame.time.Clock()
fps = 59

screen_height = 960
screen_width = 720

rows = 5 
coll = 6

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Invaders')

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
            print("Left")
            self.rect.x -= speed
        if key[pygame.K_RIGHT] and self.rect.right < screen_width:
            print("Right")
            self.rect.x += speed

        time_now = pygame.time.get_ticks()
        #shooting
        if key[pygame.K_SPACE] and time_now - self.last_shot > bulletlimiter:
            bullet = Bullets(self.rect.centerx, self.rect.top)
            bullet_group.add(bullet)
            self.last_shot = time_now
        #health bar
        pygame.draw.rect(screen, red, (self.rect.x, (self.rect.bottom + 10), self.rect.width, 15))
        if self.health_remaining > 0:
            pygame.draw.rect(screen, green, (self.rect.x, (self.rect.bottom + 10), self.rect.width * (self.health_remaining / self.health_start), 15))

#bullets
class Bullets(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("Assets\Bullet.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

    def update(self):
        self.rect.y -= 7


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
       




spaceship_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
alien_group = pygame.sprite.Group()

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

def game():
    running = True
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
        for event in pygame.event.get():
            if back_button.draw(screen):
                running = False
        pygame.display.update()
    
run = True
while run:

    clock.tick(fps)
    
    #background
    draw_background()
    
    #splashscreen
    draw_splash()

    #display buttons
    if start_button.draw(screen):
            print("Start")
            game()

    if exit_button.draw(screen):
        run = False
    if help_button.draw(screen):
        pygame.display.set_caption("Help")
        help()
    

    #event handlers
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit