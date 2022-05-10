from cgi import test
import pygame
from pygame import mixer
from pygame.locals import *
import random

pygame.init

screen_height = 960
screen_width = 720

screen = pygame.display.set_mode((screen_width, screen_height))

highlighted = pygame.image.load("Assets\Highlight.png")

def testbutton():
    screen.blit(highlighted, (90, 800))

class Button():
    def __init__(self, x, y, image, scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int (height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)
        self.clicked = False

    def draw(self, surface):
        action = False
        #click pos
        pos = pygame.mouse.get_pos()

        #click button
        if self.rect.collidepoint(pos):
            #testbutton()
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True

            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False

        surface.blit(self.image,(self.rect.x, self.rect.y))

        return action
