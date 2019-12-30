import math
import os
import sys

import pygame

FPS = 20
pygame.init()
WIDTH, HEIGHT = 1000, 600
pygame.display.set_caption('Space rangers')
screen = pygame.display.set_mode((WIDTH, HEIGHT))
player1_group = pygame.sprite.Group()
borders = pygame.sprite.Group()
clock = pygame.time.Clock()


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    image = pygame.image.load(fullname).convert()
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


class border(pygame.sprite.Sprite):
    def __init__(self, x, y, wid, hei):
        super().__init__(borders)
        self.image = pygame.Surface((wid, hei), pygame.SRCALPHA)
        self.image.fill((0, 0, 0))
        self.rect = pygame.Rect(x, y, wid, hei)
        self.mask = pygame.mask.from_surface(self.image)


class Player1(pygame.sprite.Sprite):
    orig_image = load_image("spaceship1.png", -1)
    orig_image = pygame.transform.scale(orig_image, (50, 50))

    def __init__(self):
        super().__init__(player1_group)
        self.image = Player1.orig_image
        self.rect = self.image.get_rect().move(100, 100)
        player1_group.add(self)
        self.angle = 180
        self.x = 100
        self.y = 100
        self.moving = True
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        if not pygame.sprite.spritecollide(self, borders, False, pygame.sprite.collide_mask):
            self.rect.x -= 2
            print(1)
        for bullet in bullets1:
            if pygame.sprite.spritecollide(self, [bullet], False):
                # self.kill()
                bullet.kill()
                global running
                running = False

PLAYER1 = Player1()
horiz_border = border(30, 580, 940, 3)
horiz_border2 = border(30, 30, 940, 3)
vert_border = border(30, 30, 3, 550)
vert_border2 = border(967, 30, 3, 550)
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill((255, 255, 255))
    player1_group.draw(screen)
    borders.draw(screen)
    player1_group.update()
    pygame.display.flip()
    clock.tick(FPS)
pygame.quit()
