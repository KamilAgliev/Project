import math
import os

import pygame

FPS = 60
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


class Border(pygame.sprite.Sprite):

    def __init__(self, x, y, wid, hei):
        super().__init__(borders)
        self.image = pygame.Surface([wid, hei])
        self.image.fill((0, 0, 0))
        self.rect = pygame.Rect(x, y, wid, hei)
        self.mask = pygame.mask.from_surface(self.image)


class Player1(pygame.sprite.Sprite):
    orig_image = load_image("spaceship1.png", -1)
    orig_image = pygame.transform.scale(orig_image, (50, 50))

    def __init__(self):
        super().__init__(player1_group)
        self.image = Player1.orig_image
        self.rect = self.image.get_rect().move(100, 50)
        self.angle = 90
        self.moving = True
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        for bord in borders:
            if pygame.sprite.collide_mask(self, bord):
                self.moving = False
        if self.moving:
            self.rect = self.rect.move(
                math.sin(math.radians(self.angle + 180)) * 5,
                math.cos(math.radians(self.angle + 180)) * 5)


PLAYER1 = Player1()
horiz_border = Border(30, 580, 940, 10)
horiz_border2 = Border(30, 30, 940, 10)
vert_border = Border(30, 30, 10, 550)
vert_border2 = Border(967, 30, 10, 560)
running = True
for bord1 in borders:
    print(bord1.rect)
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
