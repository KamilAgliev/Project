# importing all libraries we need
import math
import os
import random
import sys
import pygame

# global variables(groups of sprites and pygame beginnning)
FPS = 20
FPS_for_animation = 15
pygame.init()
WIDTH, HEIGHT = 1000, 600
pygame.display.set_caption('SPACE RANGERS')
screen = pygame.display.set_mode((WIDTH, HEIGHT))
player1_group = pygame.sprite.Group()
player2_group = pygame.sprite.Group()
borders = pygame.sprite.Group()
bullets1 = pygame.sprite.Group()
bullets2 = pygame.sprite.Group()
explosion_group = pygame.sprite.Group()
asteroids_group = pygame.sprite.Group()
clock = pygame.time.Clock()
cur_asteroid = 0
game_over = None
winner = None


def terminate():
    """if we close pygame window"""
    pygame.quit()
    print("getting back to desktop..")
    sys.exit(0)


def start_menu():
    """Start menu: rules and maps (in other words - starting interface)"""
    intro_text = ["SPACE RANGERS",
                  "Правила игры:",
                  "1) У каждого игрока есть космический корабль",
                  "2) При нажатии SPACE и LCTRL корабль выстреливает",
                  "3) При нажатии A и D первый корабль поворачивается в сторону",
                  "4) При нажатии RIGHT и LEFT второй корабль поворачивается в сторону",
                  "5) Цель игры: попасть снарядом в противника",
                  "6) Также вам будут мешать разные препятствия(астероиды, преграды)"]

    fon = pygame.transform.scale(load_image('background.png'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 200
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    string_rendered = font.render("Выберите карту:", 1, pygame.Color('white'))
    screen.blit(string_rendered, (350, 350))

    font_big = pygame.font.Font(None, 100)
    string_rendered = font_big.render("1", 1, pygame.Color('white'))
    screen.blit(string_rendered, (250, 450))
    string_rendered = font_big.render("2", 1, pygame.Color('white'))
    screen.blit(string_rendered, (700, 450))
    pygame.display.flip()
    coord1 = [250, 450, 275, 505]
    coord2 = [700, 450, 735, 510]
    while True:
        for event1 in pygame.event.get():
            if event1.type == pygame.QUIT:
                terminate()
            elif event1.type == pygame.MOUSEBUTTONDOWN:
                x, y = event1.pos
                if x >= coord1[0] and x <= coord1[2] and y >= coord1[1] and y <= coord1[3]:
                    return 1
                if x >= coord2[0] and x <= coord2[2] and y >= coord2[1] and y <= coord2[3]:
                    return 2


def load_image(name, colorkey=None):
    """load image from operating system function"""
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
    """Borders is an obstacle to not get out of gaming field and to make funnier"""

    def __init__(self, x, y, wid, hei, type):
        super().__init__(borders)
        self.image = pygame.Surface((wid, hei), pygame.SRCALPHA)
        self.image.fill((0, 0, 0))
        self.rect = pygame.Rect(x, y, wid, hei)
        self.mask = pygame.mask.from_surface(self.image)
        self.type = type


class Player2(pygame.sprite.Sprite):
    """Defining second player as a sprite with all it's methods"""
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
        self.magazin = 3
        self.step = 0

    def update(self):
        if self.step % 20 == 0:
            self.magazin = min(self.magazin + 1, 3)
        self.step += 1
        for bord in borders:
            if pygame.sprite.collide_mask(self, bord):
                if bord.type == 2:
                    self.rect.y += 10
                if bord.type == 1:
                    self.rect.y -= 10
                if bord.type == 3:
                    self.rect.x += 10
                if bord.type == 4:
                    self.rect.x -= 10
                self.rotating(180)
                break
        if pygame.sprite.collide_mask(self, PLAYER1):
            self.rotating(180)
        self.rect.x += math.sin(math.radians(self.angle + 180)) * 5
        self.rect.y += math.cos(math.radians(self.angle + 180)) * 5

    def rotating(self, k):
        self.angle = (self.angle + k) % 360
        self.image = pygame.transform.rotate(Player2.orig_image, self.angle)


class Player1(pygame.sprite.Sprite):
    """Defining first player as a sprite with all it's methods"""
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
        self.magazin = 3
        self.step = 0

    def update(self):
        if self.step % 20 == 0:
            self.magazin = min(self.magazin + 1, 3)
        self.step += 1
        for bord in borders:
            if pygame.sprite.collide_mask(self, bord):
                if bord.type == 2:
                    self.rect.y += 10
                if bord.type == 1:
                    self.rect.y -= 10
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
    """Spaceships can shoot and this id bullets class, where bullet defined as sprite with all it's methods"""

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
        if self.rect.x < 0 or self.rect.x > 1000 or self.rect.y < 0 or self.rect.y > 600:
            self.kill()
            return
        if self.belongs == "first":
            if pygame.sprite.collide_mask(self, PLAYER2):
                PLAYER2.kill()
                self.kill()
                global game_over, winner
                game_over = True
                winner = 1
        if self.belongs == "second":
            if pygame.sprite.collide_mask(self, PLAYER1):
                PLAYER1.kill()
                self.kill()
                game_over = True
                winner = 2
        for ast in asteroids_group:
            if pygame.sprite.collide_mask(self, ast):
                ast.kill()
                self.kill()
                return
        for bord in borders:
            if pygame.sprite.collide_mask(self, bord):
                self.kill()
                return
        self.rect = self.rect.move(
            math.sin(math.radians(self.angle + 180)) * 10,
            math.cos(math.radians(self.angle + 180)) * 10)


class Asteroid(pygame.sprite.Sprite):
    """Asteroid is an obstacle to make game longer and saturated"""
    orig_image = load_image("AsteroidBrown.png", -1)
    orig_image = pygame.transform.scale(orig_image, (40, 40))

    def __init__(self):
        super().__init__(asteroids_group)
        self.image = Asteroid.orig_image
        self.rect = self.image.get_rect()

        self.mask = pygame.mask.from_surface(self.image, pygame.SRCALPHA)
        x, y = random.randint(top_left, WIDTH - top_left * 2 - top_left), random.randint(top_up,
                                                                                         HEIGHT - top_bot * 2 - top_bot)
        self.rect.x, self.rect.y = x, y
        while True:
            x, y = random.randint(top_left, WIDTH - top_left * 2 - top_left), random.randint(top_up,
                                                                                             HEIGHT - top_bot * 2 - top_bot)
            self.rect.x = x
            self.rect.y = y
            if self.is_legit():
                break
        self.angle = random.randint(0, 360)

    def update(self):
        for bullet2 in bullets2:
            if pygame.sprite.collide_mask(self, bullet2):
                self.kill()
                bullet2.kill()
                return
        for bullet1 in bullets1:
            if pygame.sprite.collide_mask(self, bullet1):
                self.kill()
                bullet1.kill()
                return
        for bord in borders:
            if pygame.sprite.collide_mask(self, bord):
                self.angle += 180
                self.angle %= 360
                self.rect = self.rect.move(
                    math.sin(math.radians(self.angle + 180)) * 4,
                    math.cos(math.radians(self.angle + 180)) * 4)
        self.rect = self.rect.move(
            math.sin(math.radians(self.angle + 180)) * 5,
            math.cos(math.radians(self.angle + 180)) * 5)

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


class Explosion(pygame.sprite.Sprite):
    """When one of players shoots another, explosion animation appears"""

    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(explosion_group)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x - sheet.get_width() // columns / 2, y - sheet.get_height() // rows / 2)

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                cur_image = sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size))
                self.frames.append(cur_image)

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]


running = True
# infinitly repeating game process until termination
while running:
    begin = start_menu()
    get_back_to_menu = False
    # if user chose one of the maps he will play it again if clicks rematch button
    while not get_back_to_menu:
        winner = 0
        game_over = False
        PLAYER1 = Player1()
        PLAYER2 = Player2()
        top_left = 30
        top_right = 30
        top_up = 30
        top_bot = 20
        width_bord = 3
        # side borders
        horiz_border = Border(top_left, HEIGHT - top_up, WIDTH - top_left * 2 - top_left, width_bord, 1)
        horiz_border2 = Border(top_left, top_up, WIDTH - top_left * 2 - top_left, width_bord, 2)
        vert_border = Border(top_left, top_up, width_bord, HEIGHT - top_bot * 2 - top_bot, 3)
        vert_border2 = Border(WIDTH - top_left * 2, top_up, width_bord, HEIGHT - top_bot * 2 - top_bot + width_bord, 4)
        # map borders
        if begin == 1:
            horiz_border3 = Border((WIDTH - top_left * 2) / 2, (HEIGHT - top_bot * 2 - top_bot) / 2 - 130,
                                   width_bord,
                                   300,
                                   5)
            vert_border3 = Border((WIDTH - top_left * 2) / 2 - 200, (HEIGHT - top_bot * 2 - top_bot) / 2 + 30, 400,
                                  width_bord,
                                  -1)
            cur_asteroid = 0
            # creating asteroids
            for _ in range(20):
                cur_asteroid += 1
                Asteroid()
        else:
            horiz_border3 = Border((WIDTH - top_left * 2) / 2, (HEIGHT - top_bot * 2 - top_bot) / 2 - 130,
                                   width_bord,
                                   300,
                                   5)
            horiz_border4 = Border((WIDTH - top_left * 2) / 2 - 200, (HEIGHT - top_bot * 2 - top_bot) / 2 - 130,
                                   width_bord,
                                   300,
                                   6)
            horiz_border5 = Border((WIDTH - top_left * 2) / 2 + 200, (HEIGHT - top_bot * 2 - top_bot) / 2 - 130,
                                   width_bord,
                                   300,
                                   7)
            # creating asteroids
            cur_asteroid = 0
            for _ in range(15):
                cur_asteroid += 1
                Asteroid()
        a_pres = False
        d_pres = False
        right_pres = False
        left_pres = False
        print("game begins")
        # game is going on until both of the players are alive
        while not game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                # rotating processes
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a:
                        a_pres = True
                    if event.key == pygame.K_d:
                        d_pres = True
                    if event.key == pygame.K_RIGHT:
                        right_pres = True
                    if event.key == pygame.K_LEFT:
                        left_pres = True
                    # creating bullets, but in some order
                    if event.key == pygame.K_SPACE:
                        if PLAYER1.magazin > 0:
                            Bullet("first", PLAYER1.angle, PLAYER1.rect)
                            PLAYER1.magazin -= 1
                    if event.key == pygame.K_RCTRL:
                        if PLAYER2.magazin > 0:
                            Bullet("second", PLAYER2.angle, PLAYER2.rect)
                            PLAYER2.magazin -= 1
                # rotating processes
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_a:
                        a_pres = False
                    if event.key == pygame.K_d:
                        d_pres = False
                    if event.key == pygame.K_RIGHT:
                        right_pres = False
                    if event.key == pygame.K_LEFT:
                        left_pres = False
            # redrawing all sprites
            screen.fill((255, 255, 255))
            player1_group.draw(screen)
            player2_group.draw(screen)
            borders.draw(screen)
            bullets2.draw(screen)
            bullets1.draw(screen)
            asteroids_group.draw(screen)
            # updating all sprites
            player1_group.update()
            player2_group.update()
            bullets1.update()
            bullets2.update()
            asteroids_group.update()
            clock.tick(FPS)
            # rotating processes
            if a_pres:
                PLAYER1.rotating(5)
            if d_pres:
                PLAYER1.rotating(-5)
            if right_pres:
                PLAYER2.rotating(-5)
            if left_pres:
                PLAYER2.rotating(5)
            pygame.display.flip()
        print("gameover")
        game_over = False
        # making explosion animation
        if winner == 1:
            exp_x = (PLAYER2.rect.x * 2 + PLAYER2.rect.width) / 2
            exp_y = (PLAYER2.rect.y * 2 + PLAYER2.rect.height) / 2
            explosion = Explosion(load_image("explosion2.png", -1), 8, 6, exp_x, exp_y)
            while explosion.cur_frame != 44:
                clock.tick(FPS_for_animation)
                explosion_group.draw(screen)
                pygame.display.flip()
                explosion.update()
        else:
            exp_x = (PLAYER1.rect.x * 2 + PLAYER1.rect.width) / 2
            exp_y = (PLAYER1.rect.y * 2 + PLAYER1.rect.height) / 2
            explosion = Explosion(load_image("explosion2.png", -1), 8, 6, exp_x, exp_y)
            while explosion.cur_frame != 44:
                clock.tick(FPS_for_animation)
                explosion_group.draw(screen)
                pygame.display.flip()
                explosion.update()
        # clear of sprites to not draw them again
        PLAYER2.kill()
        PLAYER1.kill()
        player2_group.empty()
        player1_group.empty()
        for ast in asteroids_group:
            ast.kill()
        for bullet in bullets2:
            bullet.kill()
        for bullet in bullets1:
            bullet.kill()
        for bord in borders:
            bord.kill()
        # making interface for user, to choose what to do next(get back to menu or rematch)
        font1 = pygame.font.Font(None, 100)
        font2 = pygame.font.Font(None, 70)
        screen.blit(pygame.transform.scale(load_image("background.png"), (WIDTH, HEIGHT)), [0, 0])
        y = 200
        string_rendered = font1.render(f"Player {winner} is Winner!", 1, pygame.Color('white'))
        screen.blit(string_rendered, (200, y))
        y += 100
        string_rendered = font2.render("rematch                     back to menu", 1, pygame.Color('white'))
        screen.blit(string_rendered, (100, y))
        pygame.display.flip()
        print("closing interface")
        # waiting for user to choose
        fl = 1
        while fl:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    terminate()
                if e.type == pygame.MOUSEBUTTONDOWN:
                    x1, y1 = e.pos
                    if x1 >= 103 and x1 <= 297 and y1 >= 314 and y1 <= 340:
                        fl = 0
                    if x1 >= 575 and x1 <= 883 and y1 >= 314 and y1 <= 340:
                        fl = 0
                        get_back_to_menu = True
        if get_back_to_menu:
            print("back to menu")
        else:
            print('rematch')
        # continuing our cycle or getting back to menu
terminate()
