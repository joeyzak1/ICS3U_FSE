#levelThree.py
'''
this part of the program is just the part where you walk to the boss portion, no other obstacles
'''

from pygame import *
import shortcutFunctions

screen = display.set_mode((1024, 768))
myClock = time.Clock()

X = 0
Y = 1
W = 2
H = 3
ROW = 2
COL = 3
BOT = 2
SCREENX = 3

backPic = image.load('Backgrounds/LevelThree_BackPic.png').convert()

GROUND = 633
bottom = GROUND

v = [0, 0, bottom, 50]
jumpSpeed = -20
gravity = 1

player = [300, 600, 4, 0]
pRect = Rect(300, 600, 50, 50)

doorRect = Rect(3200, 300, 300, GROUND-300)


def drawScene(p, player, sprites, doorRect):
    global v

    offset = v[SCREENX] - p[X]
    screen.blit(backPic, (offset, 0))

    doorRect = doorRect.move(offset, 0)
    draw.rect(screen, (255, 0, 0), doorRect)

    shortcutFunctions.playerSprites(player, p, sprites, v)
    hitbox = shortcutFunctions.playerSprites(player, p, sprites, v)

    myClock.tick(60)
    display.update()

def move(p, player, sprites):
    keys = key.get_pressed()
    global v

    leftEnd = 300
    rightEnd = 3900

    if keys[K_SPACE] and p[Y] + p[H] == v[BOT] and v[Y] == 0: #fix this area
        v[Y] = jumpSpeed

    if keys[K_LEFT] and player[X] > leftEnd:
        shortcutFunctions.moveGuyLeft(p, player, v, leftEnd, rightEnd)

    elif keys[K_RIGHT] and player[X] < rightEnd:
        shortcutFunctions.moveGuyRight(p, player, v, leftEnd, rightEnd)

    else:
        player[COL] = 0
        player[COL] -= 0.2
        v[X] = 0

    player[COL] += 0.2

    if player[COL] >= len(sprites[ROW]):
        player[COL] = 1

    p[X] += v[X]
    player[X] = p[X]
    v[Y] += gravity

def check(p, player, sprites):
    global v

    shortcutFunctions.playerSprites(player, p, sprites, v)
    hitBox = shortcutFunctions.playerSprites(player, p, sprites, v)

    p[Y] += v[Y]
    player[Y] += v[Y]

    p[H] = hitBox[H]
    p[W] = hitBox[W]

    

    if p[Y] + hitBox[H] >= GROUND:
        v[BOT] = GROUND
        p[Y] = GROUND - hitBox[H]
        v[Y] = 0


