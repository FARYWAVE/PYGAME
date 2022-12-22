import os
import sys
import pygame
import math
from random import choice

world_pos = 1       # различные переменные
frames_count = 0

size = width, height = 1920, 1080  # касаемо экрана
screen = pygame.display.set_mode(size)

background_sprites = pygame.sprite.Group()  # создание групп спрайтов
player_sprite = pygame.sprite.Group()
gun_sprite = pygame.sprite.Group()
player_bullets = pygame.sprite.Group()

PLAYER_SCREEN_POS_X = 960 # позиции и скорости
PLAYER_SCREEN_POS_Y = 540
player_game_pos_x = 0
player_game_pos_y = 0
player_speed = 10
bullet_speed = 40


def position(sprite, x, y):   # функция, задающая центр объекта, относительно спавна игрока, пример:
    done = (0 - player_game_pos_x + PLAYER_SCREEN_POS_X - x,    # self.rect.center = position(self, 100, 100)
            0 - player_game_pos_y + PLAYER_SCREEN_POS_Y - y,)   # позиция спрайта будет на 100 пикселей ниже и правее координаты
                                                                # спавна
    return done


def rot_center(image, angle):                               # поворот картинки
    loc = image.get_rect().center
    rot_sprite = pygame.transform.rotate(image, angle)
    rot_sprite.get_rect().center = loc
    return rot_sprite


def load_image(name, colorkey=None):                        # загрузка картинки
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


gun_texture = load_image('M4.png')
gun_texture = pygame.transform.scale(gun_texture, (200, 200))


class Example(pygame.sprite.Sprite):       # пример спрайта и работы функции position
    im = load_image('ex.jfif')

    def __init__(self, group):
        super().__init__(group)
        self.image = self.im
        self.rect = self.im.get_rect()
        self.rect.center = position(self, 100, 100)

    def update(self):
        self.rect.center = position(self, 100, 100)


class Level(pygame.sprite.Sprite):       # класс заднего фона, в будущем не нужен
    image = load_image("background.jpg")

    def __init__(self, group):
        super().__init__(group)
        self.image = Level.image
        self.image = pygame.transform.scale(self.image, (2160, 1440))
        self.rect = self.image.get_rect()
        self.rect.center = position(self, 0, 0)

    def update(self):
        self.rect.center = position(self, 0, 0)


class Player(pygame.sprite.Sprite):       # класс игрока
    image = load_image('player_calm.png')
    player_reverse = False

    def __init__(self, group):
        super().__init__(group)
        self.image = self.image
        self.image = pygame.transform.scale(self.image, (200, 200))
        self.rect = self.image.get_rect()
        self.rect.center = (PLAYER_SCREEN_POS_X, PLAYER_SCREEN_POS_Y)

    def update(self):
        if moving_up is True or moving_down is True or moving_left is True or moving_right is True:
            if world_pos == 1:
                self.image = load_image('player_moving_1.png')
                self.image = pygame.transform.scale(self.image, (200, 200))
                if self.player_reverse is True:
                    self.image = pygame.transform.flip(self.image, True, False)
                self.rect = self.image.get_rect()
                self.rect.center = (PLAYER_SCREEN_POS_X, PLAYER_SCREEN_POS_Y)
            else:
                self.image = load_image('player_moving_2.png')
                self.image = pygame.transform.scale(self.image, (200, 200))
                if self.player_reverse is True:
                    self.image = pygame.transform.flip(self.image, True, False)
                self.rect = self.image.get_rect()
                self.rect.center = (PLAYER_SCREEN_POS_X, PLAYER_SCREEN_POS_Y)
        else:
            self.image = load_image('player_calm.png')
            self.image = pygame.transform.scale(self.image, (200, 200))
            if self.player_reverse is True:
                self.image = pygame.transform.flip(self.image, True, False)
            self.rect = self.image.get_rect()
            self.rect.center = (PLAYER_SCREEN_POS_X, PLAYER_SCREEN_POS_Y)


class M4(pygame.sprite.Sprite):     # класс валыны
    image = load_image('M4.png')

    def __init__(self, group):
        super().__init__(group)
        self.image = self.image
        self.image = pygame.transform.scale(self.image, (200, 200))
        self.rect = self.image.get_rect()
        self.rect.center = player.rect.center

    def update(self, mouse_pos):
        self.x_mouse = mouse_pos[0]
        self.y_mouse = mouse_pos[1]
        self.self_x = self.rect.center[0]
        self.self_y = self.rect.center[1]
        self.sight_x = self.self_x - self.x_mouse
        self.sight_y = self.y_mouse - self.self_y
        if self.sight_x == 0:
            self.sight_x = 0.001
        self.tg = self.sight_y / self.sight_x

        self.angle = math.degrees(math.atan(self.tg))
        if self.sight_x > 0:
            self.image = pygame.transform.flip(gun_texture, True, False)
            self.image = rot_center(self.image, self.angle)
            self.rect = self.image.get_rect()
            self.rect.center = player.rect.center
            player.player_reverse = True
        else:
            self.image = rot_center(gun_texture, self.angle)
            self.rect = self.image.get_rect()
            self.rect.center = player.rect.center
            player.player_reverse = False


class P_Bullet(pygame.sprite.Sprite):   # класс пули
    image = load_image('bullet.png')

    def __init__(self, pos):
        super().__init__(player_bullets)
        self.image = self.image
        self.rect = self.image.get_rect()
        self.rect.center = player.rect.center
        self.x_mouse = pos[0]
        self.y_mouse = pos[1]
        self.self_x = self.rect.center[0]
        self.self_y = self.rect.center[1]
        self.sight_x = self.x_mouse - self.self_x
        self.sight_y = self.y_mouse - self.self_y
        self.speed = (self.sight_x ** 2 + self.sight_y ** 2) ** (1 / 2)
        if self.speed == 0:
            self.speed = 0.01

        self.vx = bullet_speed * self.sight_x / self.speed * 2
        self.vy = bullet_speed * self.sight_y / self.speed * 2
        self.rect = self.rect.move(self.vx, self.vy)
        self.vx /= 2
        self.vy /= 2

    def update(self):
        self.rect = self.rect.move(self.vx, self.vy)


player = Player(player_sprite)              # создание спрайтов
background = Level(background_sprites)
ex = Example(background_sprites)
gun = M4(gun_sprite)

moving_up = False                   # переменные 2
moving_down = False
moving_left = False
moving_right = False
shooting = False
pos = (0, 1000)

pygame.display.set_caption('Simple Game')
clock = pygame.time.Clock()
running = True
screen.fill(pygame.Color('Black'))
while running:
    frames_count += 1                   # счетчик, использую для цикличной смены анимаций, например ходьба
    if (frames_count // 5) % 2 == 1:
        world_pos = 1
    else:
        world_pos = 0

    if shooting is True:
        P_Bullet(pos)

    background_sprites.update()       # обновление спрайтов
    player_bullets.update()
    player.update()
    background_sprites.update()

    screen.fill(pygame.Color('Black'))

    background_sprites.draw(screen)     # отрисовка
    player_bullets.draw(screen)
    player_sprite.draw(screen)
    gun_sprite.draw(screen)

    if moving_up is True:                                       # ходьба
        player_game_pos_y -= player_speed
        if not pygame.sprite.collide_mask(player, background):
            player_game_pos_y += player_speed + 2
    if moving_down is True:
        player_game_pos_y += player_speed
        if not pygame.sprite.collide_mask(player, background):
            player_game_pos_y -= (player_speed + 2)
    if moving_left is True:
        player_game_pos_x -= player_speed
        if not pygame.sprite.collide_mask(player, background):
            player_game_pos_x += player_speed + 2
    if moving_right is True:
        player_game_pos_x += player_speed
        if not pygame.sprite.collide_mask(player, background):
            player_game_pos_x -= (player_speed + 2)

    for event in pygame.event.get():            # ивенты
        if event.type == pygame.QUIT:
            running = False
            sys.exit()

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                moving_up = False
            if event.key == pygame.K_s:
                moving_down = False
            if event.key == pygame.K_a:
                moving_left = False
            if event.key == pygame.K_d:
                moving_right = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                moving_up = True
            if event.key == pygame.K_s:
                moving_down = True
            if event.key == pygame.K_a:
                moving_left = True
            if event.key == pygame.K_d:
                moving_right = True

        if event.type == pygame.MOUSEMOTION:
            pos = event.pos
            gun.update(pos)

        if event.type == pygame.MOUSEBUTTONDOWN:
            shooting = True

        if event.type == pygame.MOUSEBUTTONUP:
            shooting = False

    pygame.display.flip()
    clock.tick(30)
pygame.quit()
