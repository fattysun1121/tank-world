import pygame
import sys
import random
from pygame.locals import *


WINDOWWIDTH = 400
WINDOWHEIGHT = 400
PLAYERSPEED = 25
PLAYER_SIZE = 25
BULLETSIZE = 15
tanks = []
bullets = pygame.sprite.Group()
all_items = pygame.sprite.Group()
body_group = pygame.sprite.Group()
bullet_counter = 0
ADD_BULLET = 25


class Tank(pygame.sprite.Sprite):
    def __init__(self, dir='down', x=200, y=200, crossing=False):
        super().__init__()
        self.dir = dir
        self.crossing = crossing
        self.surfImage = {
            'up': [
                pygame.image.load(
                    'images/tank0.png'), pygame.image.load('images/tank1.png'),
                pygame.image.load(
                    'images/tank2.png'), pygame.image.load('images/tank3.png'),
                pygame.image.load('images/tank4.png')
            ],
            'down': [
                pygame.image.load(
                    'images/down0.png'), pygame.image.load('images/down1.png'),
                pygame.image.load(
                    'images/down2.png'), pygame.image.load('images/down3.png'),
                pygame.image.load('images/down4.png')

            ],
            'left': [
                pygame.image.load(
                    'images/left0.png'), pygame.image.load('images/left1.png'),
                pygame.image.load(
                    'images/left2.png'), pygame.image.load('images/left3.png'),
                pygame.image.load('images/left4.png')
            ],
            'right': [
                pygame.image.load(
                    'images/right0.png'), pygame.image.load('images/right1.png'),
                pygame.image.load(
                    'images/right2.png'), pygame.image.load('images/right3.png'),
                pygame.image.load('images/right4.png')
            ]
        }
        self.surf = pygame.transform.scale(
            self.surfImage[self.dir][0], (PLAYER_SIZE, PLAYER_SIZE))
        self.rect = pygame.Rect(x, y, PLAYER_SIZE, PLAYER_SIZE)

        self.move_count = 0

    def move(self, direction):

        self.move_count += 1
        self.surf = pygame.transform.scale(
            self.surfImage[direction][self.move_count], (PLAYER_SIZE, PLAYER_SIZE))
        if self.move_count == 4:
            self.move_count = -1
        if self.dir != direction:
            self.dir = direction
            self.rect == self.surf.get_rect(
                center=(self.rect.centerx, self.rect.centery))


class Bullet(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        bullImg = pygame.image.load(
            'images/bullet.png')
        self.surf = pygame.transform.scale(bullImg, (BULLETSIZE, BULLETSIZE))
        self.rect = pygame.Rect(
            random.randint(0 + BULLETSIZE, WINDOWWIDTH - BULLETSIZE),
            random.randint(0 + BULLETSIZE, WINDOWHEIGHT - BULLETSIZE),
            BULLETSIZE, BULLETSIZE
        )


def gen_bullet():
    bullet = Bullet()
    bullets.add(bullet)
    all_items.add(bullet)


def gen_tank():
    previous = tanks[-1]
    if previous.dir == 'up':
        body = Tank(previous.dir, previous.rect.left, previous.rect.bottom)
    elif previous.dir == 'down':
        body = Tank(previous.dir, previous.rect.left,
                    previous.rect.top - PLAYER_SIZE)
    elif previous.dir == 'left':
        body = Tank(previous.dir, previous.rect.right, previous.rect.top)
    else:
        body = Tank(previous.dir, previous.rect.left -
                    PLAYER_SIZE, previous.rect.top)
    tanks.append(body)
    body_group.add(body)
    all_items.add(body)


def move_parts():

    for i in range(len(tanks) - 1, 0, -1):
        tanks[i].move(tanks[i - 1].dir)
        tanks[i].rect.topleft = (
            tanks[i - 1].rect.left, tanks[i - 1].rect.top)


def terminate():
    pygame.quit()
    sys.exit()


pygame.init()
gameClock = pygame.time.Clock()
screen = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
pygame.display.set_caption('World of Tank')
pygame.mixer.music.load('background.mp3')
pygame.mixer.music.play(-1)
eatSound = pygame.mixer.Sound('eat.mp3')


head = Tank()

tanks.append(head)


all_items.add(head)
moveLeft = moveRight = moveUp = moveDown = False
running = True

while True:

    bullet_counter += 1
    if bullet_counter == ADD_BULLET:
        gen_bullet()
        bullet_counter = 0

    for event in pygame.event.get():
        if event.type == QUIT:
            terminate()
        elif event.type == KEYDOWN:
            if event.key == K_a:
                moveLeft = True
                moveRight = False
                moveUp = False
                moveDown = False
                crossing = False
            elif event.key == K_d:
                moveRight = True
                moveLeft = False
                moveUp = False
                moveDown = False
                crossing = False
            elif event.key == K_w:
                moveUp = True
                moveDown = False
                moveRight = False
                moveLeft = False
                crossing = False
            elif event.key == K_s:
                moveDown = True
                moveUp = False
                moveRight = False
                moveLeft = False
                crossing = False

        elif event.type == KEYUP:
            if event.key == K_ESCAPE:
                terminate()

    screen.fill((255, 255, 255))
    move_parts()
    if moveLeft:
        head.moving = True
        head.move('left')
        head.rect.move_ip(-1 * PLAYERSPEED, 0)
    elif moveRight:
        head.moving = True
        head.move('right')
        head.rect.move_ip(PLAYERSPEED, 0)
    elif moveUp:
        head.moving = True
        head.move('up')
        head.rect.move_ip(0, -1 * PLAYERSPEED)
    elif moveDown:
        head.moving = True
        head.move('down')
        head.rect.move_ip(0, PLAYERSPEED)

    for tank in tanks:
        # Connect borders.
        in_window = (tank.rect.left > 0 and tank.rect.right < WINDOWWIDTH and
                     tank.rect.top > 0 and tank.rect.bottom < WINDOWHEIGHT)

        # Record if the tank is crossing border
        # Reason: e.g. when the tank moves out from the left,
        # it'll appear at the right side and its x-coordinate
        # will be greater than WINDOWWIDTH. Hence causing the tank
        # to be transported back to the left side.
        if tank.rect.left + PLAYER_SIZE <= 0 and not tank.crossing:
            tank.rect.left = WINDOWWIDTH + tank.rect.width
            tank.crossing = True
        elif tank.rect.left >= WINDOWWIDTH and not tank.crossing:
            tank.rect.left = 0 - tank.rect.width
            tank.crossing = True
        elif tank.rect.top + PLAYER_SIZE <= 0 and not tank.crossing:
            tank.rect.top = WINDOWHEIGHT
            tank.crossing = True
        elif tank.rect.top >= WINDOWHEIGHT:
            tank.rect.bottom = 0
            tank.crossing = True
        if in_window:
            tank.crossing = False

    if pygame.sprite.spritecollideany(head, body_group):
        break
    for bullet in bullets:
        if head.rect.colliderect(bullet.rect):
            bullet.kill()
            eatSound.play()
            gen_tank()
    for item in all_items:
        screen.blit(item.surf, item.rect)

    pygame.display.update()

    gameClock.tick(5)
