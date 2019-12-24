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
        self.image = pygame.Surface([wid, hei])
        self.image.fill((0, 0, 0))
        self.rect = pygame.Rect(x, y, wid, hei)
        self.mask = pygame.mask.from_surface(self.image)


class Player1(pygame.sprite.Sprite):
    orig_image = load_image("player11.png", -1)

    def __init__(self):
        super().__init__(player1_group)
        self.image = Player1.orig_image
        self.rect = self.image.get_rect().move(50, 50)
        self.angle = 90
        self.x = 50
        self.y = 50
        self.moving = True
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        if not pygame.sprite.spritecollide(self, borders, False, pygame.sprite.collide_mask):
            self.image = pygame.transform.rotate(Player1.orig_image, self.angle)
            self.rect = self.rect.move(math.cos(math.radians(self.angle) * 10), math.sin(math.radians(self.angle) * 10))
            self.mask = pygame.mask.from_surface(self.image)


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
    pygame.display.flip()
    player1_group.update()
    clock.tick(FPS)
pygame.quit()
