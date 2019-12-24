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
player2_group = pygame.sprite.Group()
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


class Player2(pygame.sprite.Sprite):
    orig_image = load_image("player22.png", -1)

    def __init__(self):
        super().__init__(player2_group)
        self.image = Player2.orig_image
        self.rect = self.image.get_rect().move(700, 100)
        player2_group.add(self)
        self.angle = 270
        self.x = 700
        self.y = 100
        self.moving = True
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        if self.moving:
            self.image = pygame.transform.rotate(Player2.orig_image, self.angle)
            self.rect = self.image.get_rect().move(self.x, self.y)
            self.x += math.cos(math.radians(self.angle) * 40)
            self.y += math.sin(math.radians(self.angle) * 40)
            self.rect.x = self.x
            self.rect.y = self.y
        if pygame.sprite.spritecollideany(self, borders, False) \
                or pygame.sprite.spritecollideany(self, player1_group, False):
            self.moving = False
            self.x -= math.cos(math.radians(self.angle) * 40)
            self.y -= math.sin(math.radians(self.angle) * 40)
            self.rect.x = self.x
            self.rect.y = self.y

    def rotating(self, k):
        self.angle = (self.angle + k) % 360


class Player1(pygame.sprite.Sprite):
    orig_image = load_image("player11.png", -1)

    def __init__(self):
        super().__init__(player1_group)
        self.image = Player1.orig_image
        self.rect = self.image.get_rect().move(100, 100)
        player1_group.add(self)
        self.angle = 90
        self.x = 100
        self.y = 100
        self.moving = True
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        # print(self.moving, "in")
        if not self.moving:
            all_sprites = pygame.sprite.Group()
            # создадим спрайт
            sprite = pygame.sprite.Sprite()
            # определим его вид
            sprite.image = pygame.transform.rotate(Player1.orig_image, self.angle)
            # и размеры
            x, y = self.x, self.y
            sprite.rect = sprite.image.get_rect().move(x, y)
            # добавим спрайт в группу
            x += math.cos(math.radians(self.angle) * 10)
            y += math.sin(math.radians(self.angle) * 10)
            sprite.rect.x = x
            sprite.rect.y = y
            mask = pygame.mask.from_surface(sprite.image)
            ok = True
            for bord in borders:
                if pygame.sprite.collide_mask(mask, bord):
                    ok = False
            if pygame.sprite.collide_mask(mask, PLAYER2):
                ok = False
            self.moving = ok

        if self.moving:
            self.image = pygame.transform.rotate(Player1.orig_image, self.angle)
            self.rect = self.image.get_rect().move(self.x, self.y)
            self.x += math.cos(math.radians(self.angle) * 10)
            self.y += math.sin(math.radians(self.angle) * 10)
            self.rect.x = self.x
            self.rect.y = self.y
            for bord in borders:
                if pygame.sprite.collide_mask(self, bord):
                    self.moving = False
            if pygame.sprite.collide_mask(self, PLAYER2):
                    self.moving = False

        # if pygame.sprite.spritecollideany(self, borders, False) \
        #         or pygame.sprite.spritecollideany(self, player2_group, False):
        #     self.moving = False
            # self.x -= math.cos(math.radians(self.angle) * 10)
            # self.y -= math.sin(math.radians(self.angle) * 10)
            # self.rect.x = self.x
            # self.rect.y = self.y
        # print(self.moving, "out")
        print(self.x, self.y)

    def rotating(self, k):
        self.angle += k % 360


PLAYER1 = Player1()
PLAYER2 = Player2()

horiz_border = border(30, 580, 940, 3)
horiz_border2 = border(30, 30, 940, 3)
vert_border = border(30, 30, 3, 550)
vert_border2 = border(967, 30, 3, 550)

# background = load_image("background.png")

running = True
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
            if event.key == pygame.K_LEFT:
                right_pres = True
            if event.key == pygame.K_RIGHT:
                left_pres = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                a_pres = False
            if event.key == pygame.K_d:
                d_pres = False
            if event.key == pygame.K_LEFT:
                right_pres = False
            if event.key == pygame.K_RIGHT:
                left_pres = False

    screen.fill((255, 255, 255))
    # screen.blit(background, [0, 0])
    player1_group.draw(screen)
    player2_group.draw(screen)
    borders.draw(screen)

    pygame.display.flip()
    player1_group.update()
    player2_group.update()
    if a_pres:
        PLAYER1.angle += 1
        PLAYER1.angle %= 360
    if d_pres:
        PLAYER1.angle -= 1
        PLAYER1.angle %= 360
    if right_pres:
        PLAYER2.angle -= 1
        PLAYER2.angle %= 360
    if left_pres:
        PLAYER2.angle += 1
        PLAYER2.angle %= 360

    clock.tick(FPS)
pygame.quit()
