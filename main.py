import pygame, sys, time
from pygame.locals import *



WINDOWWIDTH = 400
WINDOWHEIGHT = 400
PLAYERSPEED = 2


def terminate():
    pygame.quit()
    sys.exit()


class Tank(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surfImage = {
            'up': [
                pygame.image.load('images/tank0.png'), pygame.image.load('images/tank1.png'),
                pygame.image.load('images/tank2.png'), pygame.image.load('images/tank3.png'),
                pygame.image.load('images/tank4.png')
            ],
            'down': [
                pygame.image.load('images/down0.png'), pygame.image.load('images/down1.png'),
                pygame.image.load('images/down2.png'), pygame.image.load('images/down3.png'),
                pygame.image.load('images/down4.png')

            ],
            'left': [
                pygame.image.load('images/left0.png'), pygame.image.load('images/left1.png'),
                pygame.image.load('images/left2.png'), pygame.image.load('images/left3.png'),
                pygame.image.load('images/left4.png')
            ],
            'right': [
                pygame.image.load('images/right0.png'), pygame.image.load('images/right1.png'),
                pygame.image.load('images/right2.png'), pygame.image.load('images/right3.png'),
                pygame.image.load('images/right4.png')
            ]
            }
        self.surf = pygame.transform.scale(self.surfImage['up'][0], (32, 32))
        self.rect = pygame.Rect(200, 200, 32, 32)
        self.moving = False
        self.has_fire = False
        self.move_count = 0
        self.fire_count = 0
        self.dir = 'up'

    def move(self, direction):
        if self.moving:
            self.move_count += 1
            self.surf = pygame.transform.scale(self.surfImage[direction][self.move_count], (32, 32))
            if self.move_count == 4:
                self.move_count = -1
        if self.dir != direction:
            self.dir = direction
            self.rect == self.surf.get_rect(center=(self.rect.centerx, self.rect.centery))

    def fire(self):
        if player.has_fire:
            self.fire_count += 1
            if self.fire_count == 5:
                self.fire_count = 0

                if self.dir == 'up':
                    filename = 'tank0'
                elif self.dir in ['down', 'left', 'right']:
                    filename = self.dir + '0'
                orgImg = pygame.image.load('images/%s.png' %(filename))
                self.surf = pygame.transform.scale(orgImg, (32, 32))
                player.has_fire = False

        else:
            if self.dir == 'up':
                filename = 'tankf'
            elif self.dir in ['down', 'left', 'right']:
                filename = self.dir + 'f'
            fireImg = pygame.image.load('images/%s.png' %(filename))
            self.surf = pygame.transform.scale(fireImg, (32, 32))







pygame.init()
gameClock = pygame.time.Clock()
screen = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
pygame.display.set_caption('World of Tank')


player = Tank()

moveLeft = moveRight = moveUp = moveDown = False

while True:



    for event in pygame.event.get():
        if event.type == QUIT:
            terminate()
        elif event.type == KEYDOWN:
            if event.key == K_a:
                moveLeft = True
                moveRight = False
                moveUp = False
                moveDown = False
            elif event.key == K_d:
                moveRight = True
                moveLeft = False
                moveUp = False
                moveDown = False
            elif event.key == K_w:
                moveUp = True
                moveDown = False
                moveRight = False
                moveLeft = False
            elif event.key == K_s:
                moveDown = True
                moveUp = False
                moveRight = False
                moveLeft = False
            if event.key == K_k:
                player.fire()
                player.has_fire = True
        elif event.type == KEYUP:
            if event.key == K_ESCAPE:
                terminate()

            elif event.key == K_a:
                moveLeft = False
            elif event.key == K_d:
                moveRight = False

            elif event.key == K_w:
                moveUp = False

            elif event.key == K_s:
                moveDown = False


    if player.has_fire:
        player.fire()


    if moveLeft:
        player.moving = True
        player.move('left')
        player.rect.move_ip(-1 * PLAYERSPEED, 0)

    elif moveRight:
        player.moving = True
        player.move('right')
        player.rect.move_ip(PLAYERSPEED, 0)

    elif moveUp:
        player.moving = True
        player.move('up')
        player.rect.move_ip(0, -1 * PLAYERSPEED)

    elif moveDown:
        player.moving = True
        player.move('down')

        player.rect.move_ip(0, PLAYERSPEED)






    screen.fill((255, 255, 255))

    screen.blit(player.surf, player.rect)
    pygame.display.update()

    gameClock.tick(30)



