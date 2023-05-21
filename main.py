from CONSTANTS import *
import sys
import time
import random
import pygame
import math
from pygame.locals import *

pygame.init()

screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption('Flappy Hair')

# main menu screen
MAIN_MENU_BACK = pygame.image.load(MENU_BACK_path)
MAIN_MENU_BACK = pygame.transform.scale(MAIN_MENU_BACK, SCREEN_SIZE)
screen.blit(MAIN_MENU_BACK, (0, 0))

# game screen
GAME_BG = pygame.image.load(INGAME_BACK_path)
GAME_BG = pygame.transform.scale(GAME_BG, (1500, 1080))
game_bg_width = GAME_BG.get_width()

# variables
fps = 60
font = pygame.font.Font('Font/HairyBeard.ttf', 200)
clock = pygame.time.Clock()
ball = pygame.Rect(WIDTH / 2 - 15, HEIGHT / 2 - 15, 30, 30)
main_menu = True
tiles = math.ceil(WIDTH / game_bg_width) + 1
scroll = 0

logo = font.render(str('FLAPPY HAIR'), 1, (200, 200, 200))
screen.blit(logo, (470, 150))
pygame.display.flip()


# Bird class
class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.index = 0
        self.counter = 0
        for num in range(1, 4):
            img = pygame.image.load(f'images/amr_ball_{num}.png')
            self.images.append(img)
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.vel = 0
        self.clicked = False

    def update(self):
        # gravity
        global location
        self.vel += 0.3
        if self.vel > 8:
            self.vel = 8

        if self.rect.bottom < 935:
            self.rect.y += int(self.vel)
        # elif self.rect.top <= 0:
        #     self.vel = 10
        #     self.rect.y += int(self.vel)

        # jump
        move_ticker = 0
        if move_ticker > 0:
            move_ticker -= 1

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and self.clicked == False and self.rect.top > 5:
                if move_ticker == 0:
                    move_ticker = 10
                    self.clicked = True
                    self.vel = -10
                    self.rect.y += int(self.vel)

        # if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False and self.rect.top > 50:
        #     self.clicked = True
        #     self.vel = -10
        #     self.rect.y += int(self.vel)

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        # handle the animation
        self.counter += 1
        flap_cooldown = 100
        if self.counter > flap_cooldown:
            self.counter = 0
            self.index += 1
            if self.index >= len(self.images):
                self.index = 0
        self.image = self.images[self.index]


bird_group = pygame.sprite.Group()
flappy = Bird(300, int(HEIGHT / 2))
bird_group.add(flappy)

# game loop
run = True
while run:
    ev = pygame.event.get()
    clock.tick(fps)
    for event in ev:
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            print(pos)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                main_menu = False
    if not main_menu:

        for i in range(0, tiles):
            screen.blit(GAME_BG, (i * game_bg_width + scroll, 0))
            bird_group.draw(screen)
            bird_group.update()
            pygame.display.flip()

        scroll -= 5

        # reset scroll
        if abs(scroll) > game_bg_width:
            scroll = 0

pygame.quit()
sys.exit()
