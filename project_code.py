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
asteroids_group = pygame.sprite.Group()
clock = pygame.time.Clock()
game_over = False
cur_asteroid = 0


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
    def __init__(self, x, y, wid, hei, type):
        super().__init__(borders)
        self.image = pygame.Surface((wid, hei), pygame.SRCALPHA)
        self.image.fill((0, 0, 0))
        self.rect = pygame.Rect(x, y, wid, hei)
        self.mask = pygame.mask.from_surface(self.image)
        self.type = type


class Player2(pygame.sprite.Sprite):
    orig_image = load_image("spaceship2.png", -1)
    orig_image = pygame.transform.scale(orig_image, (50, 50))

    def __init__(self):
        super().__init__(player2_group)
        self.image = Player2.orig_image
        self.rect = self.image.get_rect().move(800, 500)
        player2_group.add(self)
        self.angle = 270
        self.mask = pygame.mask.from_surface(self.image, pygame.SRCALPHA)
        self.image = pygame.transform.rotate(Player2.orig_image, self.angle)

    def update(self):
        for bord in borders:
            if pygame.sprite.collide_mask(self, bord):
                self.rotating(180)
                self.image = pygame.transform.rotate(Player2.orig_image, self.angle)
                break
        if pygame.sprite.collide_mask(self, PLAYER1):
            self.rotating(180)
        self.rect.x += math.sin(math.radians(self.angle + 180)) * 5
        self.rect.y += math.cos(math.radians(self.angle + 180)) * 5

    def rotating(self, k):
        self.angle = (self.angle + k) % 360
        self.image = pygame.transform.rotate(Player2.orig_image, self.angle)


class Player1(pygame.sprite.Sprite):
    orig_image = load_image("spaceship1.png", -1)
    orig_image = pygame.transform.scale(orig_image, (50, 50))

    def __init__(self):
        super().__init__(player1_group)
        self.image = Player1.orig_image
        self.rect = self.image.get_rect().move(100, 100)
        player1_group.add(self)
        self.angle = 90
        self.mask = pygame.mask.from_surface(self.image, pygame.SRCALPHA)
        self.image = pygame.transform.rotate(Player1.orig_image, self.angle)

    def update(self):
        for bord in borders:
            if pygame.sprite.collide_mask(self, bord):
                if bord.type == 1:
                    self.rect.y -= 10
                if bord.type == 2:
                    self.rect.y += 10
                if bord.type == 3:
                    self.rect.x += 10
                if bord.type == 4:
                    self.rect.x -= 10
                self.rotating(180)
                break
        if pygame.sprite.collide_mask(self, PLAYER2):
            self.rotating(180)
        self.rect.x += math.sin(math.radians(self.angle + 180)) * 5
        self.rect.y += math.cos(math.radians(self.angle + 180)) * 5

    def rotating(self, k):
        self.angle = (self.angle + k) % 360
        self.image = pygame.transform.rotate(Player1.orig_image, self.angle)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, belongs, angle, rect):
        super().__init__()
        self.angle = angle
        self.radius = 5
        self.image = pygame.Surface((2 * self.radius, 2 * self.radius), pygame.SRCALPHA, 32)
        self.rect = rect.move(50 * math.sin(math.radians(self.angle + 180)),
                              50 * math.cos(math.radians(self.angle + 180)))
        self.belongs = belongs
        if belongs == "first":
            pygame.draw.circle(self.image, pygame.Color("blue"), (self.radius, self.radius), self.radius)
            bullets1.add(self)
        else:
            pygame.draw.circle(self.image, pygame.Color("green"), (self.radius, self.radius), self.radius)
            bullets2.add(self)
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.rect = self.rect.move(
            math.sin(math.radians(self.angle + 180)) * 10,
            math.cos(math.radians(self.angle + 180)) * 10)
        for bord in borders:
            if pygame.sprite.collide_mask(self, bord):
                self.kill()
        if self.belongs == "first":
            if pygame.sprite.collide_mask(self, PLAYER2):
                PLAYER2.kill()
                self.kill()
        if self.belongs == "second":
            if pygame.sprite.collide_mask(self, PLAYER1):
                PLAYER1.kill()
                self.kill()


class Asteroid(pygame.sprite.Sprite):
    orig_image = load_image("AsteroidBrown.png", -1)
    orig_image = pygame.transform.scale(orig_image, (30, 30))

    def __init__(self):
        super().__init__(asteroids_group)
        asteroids_group.add(self)
        self.image = Asteroid.orig_image
        self.rect = self.image.get_rect()

        self.mask = pygame.mask.from_surface(self.image, pygame.SRCALPHA)
        x, y = random.randint(40, 1000), random.randint(30, 600)
        self.rect.x, self.rect.y = x, y
        while True:
            x, y = random.randint(40, 1000), random.randint(30, 600)
            self.rect.x = x
            self.rect.y = y
            if self.is_legit():
                break
        self.vx = random.randint(-5, 5)
        self.vy = random.randrange(-5, 5)

    def update(self):
        for bullet in bullets2:
            if pygame.sprite.collide_mask(self, bullet):
                self.kill()
                bullet.kill()
        for bullet in bullets2:
            if pygame.sprite.collide_mask(self, bullet):
                self.kill()
                bullet.kill()
        for bord in borders:
            if pygame.sprite.collide_mask(self, bord):
                if bord.type <= 2:
                    self.vy *= -1
                else:
                    self.vx *= -1
        self.rect = self.rect.move(self.vx, self.vy)

    def is_legit(self):
        ok = True
        cur = 0
        for ast in asteroids_group:
            if cur == cur_asteroid - 1:
                break
            if pygame.sprite.collide_mask(self, ast):
                ok = False
            cur += 1
        for bord in borders:
            if pygame.sprite.collide_mask(self, bord):
                ok = False
        if pygame.sprite.collide_mask(self, PLAYER1):
            ok = False
        if pygame.sprite.collide_mask(self, PLAYER2):
            ok = False
        return ok


PLAYER1 = Player1()
PLAYER2 = Player2()
horiz_border = Border(30, 580, 940, 3, 1)
horiz_border2 = Border(30, 30, 940, 3, 2)
vert_border = Border(30, 30, 3, 550, 3)
vert_border2 = Border(967, 30, 3, 550, 4)
for _ in range(20):
    cur_asteroid += 1
    Asteroid()
running = True

# start_menu()
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
            if event.key == pygame.K_RIGHT:
                right_pres = True
            if event.key == pygame.K_LEFT:
                left_pres = True
            if event.key == pygame.K_SPACE:
                Bullet("first", PLAYER1.angle, PLAYER1.rect)
            if event.key == pygame.K_RCTRL:
                Bullet("second", PLAYER2.angle, PLAYER2.rect)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                a_pres = False
            if event.key == pygame.K_d:
                d_pres = False
            if event.key == pygame.K_RIGHT:
                right_pres = False
            if event.key == pygame.K_LEFT:
                left_pres = False

    screen.fill((255, 255, 255))
    player1_group.draw(screen)
    player2_group.draw(screen)
    borders.draw(screen)
    bullets2.draw(screen)
    bullets1.draw(screen)
    asteroids_group.draw(screen)
    pygame.display.flip()
    player1_group.update()
    player2_group.update()
    bullets1.update()
    bullets2.update()
    asteroids_group.update()
    clock.tick(FPS)
    if a_pres:
        PLAYER1.rotating(5)
    if d_pres:
        PLAYER1.rotating(-5)
    if right_pres:
        PLAYER2.rotating(-5)
    if left_pres:
        PLAYER2.rotating(5)
    pygame.display.flip()
pygame.quit()
