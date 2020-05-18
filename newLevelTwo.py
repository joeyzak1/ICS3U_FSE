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

plats = [Rect(600, 375, 200, 15), Rect(1550, 375, 200, 15), Rect(8000, 200, 200, 15), Rect(8650, 200, 200, 15), 
        Rect(9050, 287, 200, -15)]

#this list branches off into 2 2d lists one for ground spikes and one for wall spikes
spikes = [[Rect(800, GROUND, 400, -50), Rect(3400, 275, 400, 50), Rect(3900, 475, 200, -50),
        Rect(5400, 174, 200, 50), Rect(6000, 174, 200, 50), Rect(8550, GROUND, 400, -50)],
        [Rect(1900, GROUND, 75, -300), Rect(8350, GROUND, 75, -475), Rect(9400, 374, 75, -475)]]

birds = [Rect(9600, 50, 60, 30)]

borders = [Rect(2800, 475, 2375, GROUND-475), Rect(2800, 275, 2100, -275), Rect(4900, 174, 2500, -174),
            Rect(5175, GROUND, 100, -200), Rect(5275, 374, 2875, GROUND-374)]


def drawScene(p, sprites, plats, spikes, borders, birds):
    global vPlayer

    offset = vPlayer[SCREENX] - p[X]
    screen.blit(backPic, (offset, 0))

    shortcutFunctions.drawPlats(plats, offset)
    shortcutFunctions.drawSpikes(spikes, offset)
    shortcutFunctions.drawBorders(borders, offset)
    shortcutFunctions.drawTempBird(birds, offset)

    shortcutFunctions.playerSprites(p, sprites, vPlayer)
    hitBox = shortcutFunctions.playerSprites(p, sprites, vPlayer)
    draw.rect(screen, (255, 0, 0), [vPlayer[SCREENX], hitBox[Y], hitBox[W], hitBox[H]], 2)

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


def moveBad(player, bird):
    shortcutFunctions.moveBird(player, birds)




def check(p, sprites, plats):
    global vPlayer

    shortcutFunctions.playerSprites(p, sprites, vPlayer)
    hitBox = shortcutFunctions.playerSprites(p, sprites, vPlayer)

    shortcutFunctions.checkPlats(plats, hitBox, vPlayer)

    p[Y] += vPlayer[Y]

    

    if p[Y] + hitBox[H] >= GROUND:
        vPlayer[BOT] = GROUND
        p[Y] = GROUND - hitBox[H]
        vPlayer[Y] = 0