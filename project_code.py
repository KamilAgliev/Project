import math
import os
import random

import pygame

FPS = 10
pygame.init()
WIDTH, HEIGHT = 1000, 600
pygame.display.set_caption('Space rangers')
screen = pygame.display.set_mode((WIDTH, HEIGHT))
player1_group = pygame.sprite.Group()
player2_group = pygame.sprite.Group()
borders = pygame.sprite.Group()
bullets1 = pygame.sprite.Group()
bullets2 = pygame.sprite.Group()
asteroids = pygame.sprite.Group()
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


class Player2(pygame.sprite.Sprite):
    orig_image = load_image("spaceship2.png", -1)
    orig_image = pygame.transform.scale(orig_image, (50, 50))

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
        for bullet in bullets1:
            if pygame.sprite.spritecollide(self, [bullet], False):
                self.kill()
                bullet.kill()
                global running
                running = False

        if self.moving:
            self.image = pygame.transform.rotate(Player2.orig_image, self.angle)
            self.rect = self.image.get_rect().move(self.x, self.y)
            self.x += math.sin(math.radians(self.angle + 180)) * 5
            self.y += math.cos(math.radians(self.angle + 180)) * 5
            self.rect.x = self.x
            self.rect.y = self.y
        if pygame.sprite.spritecollideany(self, borders, False) \
                or pygame.sprite.spritecollideany(self, player1_group, False):
            self.moving = False
            self.x -= math.cos(math.radians(self.angle + 180)) * 5
            self.y -= math.sin(math.radians(self.angle + 180)) * 5
            self.rect.x = self.x
            self.rect.y = self.y

    def rotating(self, k):
        self.angle = (self.angle + k) % 360


class Player1(pygame.sprite.Sprite):
    orig_image = load_image("spaceship1.png", -1)
    orig_image = pygame.transform.scale(orig_image, (50, 50))

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
        # is next step possible?
        if not self.moving:
            # создадим спрайт
            sprite = pygame.sprite.Sprite()
            # определим его вид
            sprite.image = pygame.transform.rotate(Player1.orig_image,
                                                   self.angle)
            # и размеры
            x, y = self.x, self.y
            sprite.rect = sprite.image.get_rect().move(x, y)
            # добавим спрайт в группу
            x += math.cos(math.radians(self.angle + 180)) * 5
            y += math.sin(math.radians(self.angle + 180)) * 5
            sprite.rect.x = x
            sprite.rect.y = y
            sprite.mask = pygame.mask.from_surface(sprite.image)
            ok = True
            for bord in borders:
                if pygame.sprite.collide_mask(sprite, bord):
                    ok = False
            if pygame.sprite.collide_mask(sprite, PLAYER2):
                ok = False
            self.moving = ok
        # moving
        if self.moving:
            self.image = pygame.transform.rotate(Player1.orig_image, self.angle)
            self.rect = self.image.get_rect().move(self.x, self.y)
            self.x += math.sin(math.radians(self.angle + 180)) * 5
            self.y += math.cos(math.radians(self.angle + 180)) * 5
            self.rect.x = self.x
            self.rect.y = self.y
            for bord in borders:
                if pygame.sprite.collide_mask(self, bord):
                    self.moving = False
            if pygame.sprite.collide_mask(self, PLAYER2):
                self.moving = False

    def rotating(self, k):
        self.angle = (self.angle + k) % 360
        print(self.angle)
        if self.angle == 270:
            print(self.x, self.y)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, belongs, angle, x, y):
        super().__init__()
        self.angle = angle
        self.radius = 5
        self.image = pygame.Surface((2 * self.radius, 2 * self.radius),
                                    pygame.SRCALPHA,
                                    32)
        pygame.draw.circle(self.image, pygame.Color("red"),
                           (self.radius, self.radius),
                           self.radius)
        x += math.sin(math.radians(self.angle + 180)) * 53
        y += math.cos(math.radians(self.angle + 180)) * 38
        self.rect = pygame.Rect(x, y, 2 * self.radius, 2 * self.radius)
        self.moving = True
        if belongs == "first":
            bullets1.add(self)
        else:
            bullets2.add(self)

    def update(self):
        self.rect = self.rect.move(
            math.sin(math.radians(self.angle + 180)) * 10,
            math.cos(math.radians(self.angle + 180)) * 10)
        for bord in borders:
            if pygame.sprite.collide_mask(self, bord):
                self.kill()
        if self.rect.x < 0 or self.rect.x > WIDTH or self.rect.y < 0 or self.rect.y > HEIGHT:
            self.kill()


class Asteroid(pygame.sprite.Sprite):
    orig_image = load_image("AsteroidBrown.png", -1)
    orig_image = pygame.transform.scale(orig_image, (10, 10))

    def __init__(self):
        super().__init__(asteroids)
        self.image = Asteroid.orig_image
        x, y = random.randint(), random.randint()
        while collide:
            x, y = random.randint(), random.randint()
        self.rect = self.image.get_rect().move(x, y)
        self.vx = random.randint(-5, 5)
        self.vy = random.randrange(-5, 5)

    def update(self):
        self.rect = self.rect.move(self.vx, self.vy)


PLAYER1 = Player1()
PLAYER2 = Player2()

horiz_border = Border(30, 580, 940, 3)
horiz_border2 = Border(30, 30, 940, 3)
vert_border = Border(30, 30, 3, 550)
vert_border2 = Border(967, 30, 3, 550)

for _ in range(10):
    aster = Asteroid()
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
            if event.key == pygame.K_SPACE:
                Bullet("first", PLAYER1.angle, PLAYER1.x, PLAYER1.y)
            if event.key == pygame.K_RCTRL:
                Bullet("second", PLAYER2.angle, PLAYER2.x, PLAYER2.y)
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
    bullets1.draw(screen)
    bullets2.draw(screen)

    pygame.display.flip()
    player1_group.update()
    player2_group.update()
    bullets1.update()
    bullets2.update()
    asteroids.update()
    if a_pres:
        PLAYER1.rotating(5)
    if d_pres:
        PLAYER1.rotating(-5)
    if right_pres:
        PLAYER2.rotating(5)
    if left_pres:
        PLAYER2.rotating(-5)
    clock.tick(FPS)
pygame.quit()
