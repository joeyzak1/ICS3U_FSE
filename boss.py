#boss.py

from pygame import *
import shortcutFunctions

screen = display.set_mode((1024, 768))
myClock = time.Clock()

backPic = image.load('Backgrounds/bossBack.png').convert()

X = 0
Y = 1
W = 2
H = 3
ROW = 2
COL = 3
BOT = 2

GROUND = 722
bottom = GROUND

jumpSpeed = -20
gravity = 1

player = [150, 650, 4, 0]
pRect = Rect(150, 650, 20, 45)

vPlayer = [0, 0, bottom]

def drawScene(p, player, sprites):
    global vPlayer

    screen.blit(backPic, (0, 0))

    shortcutFunctions.playerSprites(player, p, sprites, vPlayer, p[X])
    hitbox = shortcutFunctions.playerSprites(player, p, sprites, vPlayer, p[X])

    display.update()
    myClock.tick(60)

def moveGuy(p, player, sprites):
    global vPlayer

    keys = key.get_pressed()


    leftEnd = 46
    rightEnd = 978

    if keys[K_SPACE] and p[Y] + p[H] == vPlayer[BOT] and vPlayer[Y] == 0: #fix this area
        vPlayer[Y] = jumpSpeed

    if keys[K_LEFT] and p[X] > leftEnd:
        shortcutFunctions.moveGuyLeftBoss(p, player, vPlayer, leftEnd, rightEnd)

    elif keys[K_RIGHT] and p[X] < rightEnd:
        shortcutFunctions.moveGuyRightBoss(p, player, vPlayer, leftEnd, rightEnd)

    else:
        player[COL] = 0
        player[COL] -= 0.2
        vPlayer[X] = 0

    player[COL] += 0.2

    if player[COL] >= len(sprites[ROW]):
        player[COL] = 1

    p[X] += vPlayer[X]
    player[X] = p[X]
    vPlayer[Y] += gravity

def moveBoss():
    screen.fill((0))

def checkCollision(p, player, sprites):
    keys = key.get_pressed()

    global vPlayer

    shortcutFunctions.playerSprites(player, p, sprites, vPlayer, p[X])
    hitBox = shortcutFunctions.playerSprites(player, p, sprites, vPlayer, p[X])

    p[Y] += vPlayer[Y]
    player[Y] += vPlayer[Y]

    p[H] = hitBox[H]
    p[W] = hitBox[W]


    if p[Y] + hitBox[H] >= GROUND:
        vPlayer[BOT] = GROUND
        p[Y] = GROUND - hitBox[H]
        vPlayer[Y] = 0