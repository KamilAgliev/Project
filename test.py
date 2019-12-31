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


def start_menu():
    pass


class border(pygame.sprite.Sprite):
    def __init__(self, x, y, wid, hei, type):
        super().__init__(borders)
        self.image = pygame.Surface((wid, hei), pygame.SRCALPHA)
        self.image.fill((0, 0, 0))
        self.rect = pygame.Rect(x, y, wid, hei)
        self.mask = pygame.mask.from_surface(self.image)
        self.type = type


class Player1(pygame.sprite.Sprite):
    orig_image = load_image("spaceship1.png", -1)
    orig_image = pygame.transform.scale(orig_image, (50, 50))

    def __init__(self):
        super().__init__(player1_group)
        self.image = Player1.orig_image
        self.rect = self.image.get_rect().move(300, 300)
        player1_group.add(self)
        self.angle = 90
        self.moving = True
        self.mask = pygame.mask.from_surface(self.image, pygame.SRCALPHA)
        self.vector_x = 1
        self.vector_y = 1
        self.image = pygame.transform.rotate(Player1.orig_image, self.angle)

    def update(self):
        for bord in borders:
            if pygame.sprite.collide_mask(self, bord):
                self.angle += 180
                self.angle %= 360
                self.image = pygame.transform.rotate(Player1.orig_image, self.angle)
                break
        self.rect.x += self.vector_x * math.sin(math.radians(self.angle + 180)) * 5
        self.rect.y += self.vector_y * math.cos(math.radians(self.angle + 180)) * 5

    def rotating(self, k):
        self.angle = (self.angle + k) % 360
        self.image = pygame.transform.rotate(Player1.orig_image, self.angle)


PLAYER1 = Player1()
horiz_border = border(30, 580, 940, 3, 1)
horiz_border2 = border(30, 30, 940, 3, 2)
vert_border = border(30, 30, 3, 550, 3)
vert_border2 = border(967, 30, 3, 550, 4)
running = True
start_menu()
a_pres = False
d_pres = False
right_pres = False
left_pres = False
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                a_pres = True
            if event.key == pygame.K_d:
                d_pres = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                a_pres = False
            if event.key == pygame.K_d:
                d_pres = False
    screen.fill((255, 255, 255))
    player1_group.draw(screen)
    borders.draw(screen)
    player1_group.update()

    clock.tick(FPS)
    if a_pres:
        PLAYER1.rotating(5)
    if d_pres:
        PLAYER1.rotating(-5)
    pygame.display.flip()
pygame.quit()
