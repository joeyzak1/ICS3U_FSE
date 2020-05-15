#newLevelTwo.py

from pygame import *
import shortcutFunctions

screen = display.set_mode((1024, 768))
myClock = time.Clock()

backPic = image.load('Backgrounds/LevelTwo_backPic.png').convert()

GROUND = 574
bottom = GROUND

jumpSpeed = -20
gravity = 1

X = 0
Y = 1
W = 2
H = 3
ROW = 2
COL = 3
SCREENX = 3
BOT = 2

vPlayer = [0, 0, bottom, 250]

player = [250, 529, 4, 0]

plats = [Rect(600, 375, 200, 15)]

#this list branches off into 2 2d - one for ground spikes and one for wall spikes
spikes = [[Rect(800, GROUND, 400, -50)], [Rect(1900, GROUND, 75, -300)]]


def drawScene(p, sprites, plats, spikes):
    offset = vPlayer[SCREENX] - p[X]
    screen.blit(backPic, (offset, 0))

    shortcutFunctions.drawPlats(plats, offset)
    shortcutFunctions.drawSpikes(spikes, offset)

    shortcutFunctions.playerSprites(p, sprites)
    hitBox = shortcutFunctions.playerSprites(p, sprites)
    draw.rect(screen, (255, 0, 0), hitBox, 2)

    display.update()
    myClock.tick(60)

def move(p, sprites):
    global vPlayer
    keys = key.get_pressed()

    if keys[K_SPACE]:
        vPlayer[Y] = jumpSpeed

    if keys[K_LEFT] and p[X] < 400:
        shortcutFunctions.moveGuyLeft(p, vPlayer)

        # p[ROW] = 3

        # if keys[K_LSHIFT] or keys[K_RSHIFT]:
        #     vPlayer[X] = -10

        # else:
        #     vPlayer[X] = -5

        # if vPlayer[SCREENX] > 350:
        #     vPlayer[SCREENX] -= 5

    elif keys[K_RIGHT]:
        shortcutFunctions.moveGuyRight(p, vPlayer)

    else:
        p[COL] = 0
        p[COL] -= 0.2
        vPlayer[X] = 0

    p[COL] += 0.2

    if p[COL] >= len(sprites[ROW]):
        p[COL] = 1

    p[X] += vPlayer[X]
    vPlayer[Y] += gravity

def check(p, sprites):
    shortcutFunctions.playerSprites(p, sprites)
    hitBox = shortcutFunctions.playerSprites(p, sprites)

    p[Y] += vPlayer[Y]

    if p[Y] + hitBox[H] >= GROUND:
        vPlayer[BOT] = GROUND
        p[Y] = GROUND - hitBox[H]
        vPlayer[Y] = 0






