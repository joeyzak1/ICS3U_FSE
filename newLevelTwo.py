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
TOP = 4

vPlayer = [0, 0, bottom, 250, 0]

player = [250, 529, 4, 0]
pRect = Rect(250, 529, 4, 0)

plats = [Rect(600, 375, 200, 15), Rect(1550, 375, 200, 15), Rect(8000, 200, 200, 15), Rect(8650, 200, 200, 15), 
        Rect(9050, 287-15, 200, 15)]

#this list branches off into 2 2d lists one for ground spikes and one for wall spikes
spikes = [[Rect(800, GROUND, 400, -50), Rect(3400, 275, 400, 50), Rect(3900, 475, 200, -50),
        Rect(5400, 174, 200, 50), Rect(6000, 174, 200, 50), Rect(8550, GROUND, 400, -50)],
        [Rect(1900, GROUND, 75, -300), Rect(8350, GROUND, 75, -475), Rect(9400, 374, 75, -475)]]

birds = [Rect(2800, 50, 60, 30), Rect(9600, 50, 60, 30)]

borders = [Rect(2800, 475, 2375, GROUND-475), Rect(2800, 275, 2100, -275), Rect(4900, 174, 2500, -174),
            Rect(5175, GROUND, 100, -200), Rect(5275, 374, 2875, GROUND-374)]

#seperating borders into 2d lists
borders = [[Rect(2800, 475, 2375, 99), Rect(5175, 374, 100, 200), Rect(5275, 374, 2875, 200)],
            [Rect(2800, 0, 2100, 275), Rect(4900, 0, 2500, 174)]]

def drawScene(p, player, sprites, plats, spikes, borders, birds):
    global vPlayer

    offset = vPlayer[SCREENX] - p[X]
    screen.blit(backPic, (offset, 0))

    shortcutFunctions.drawPlats(plats, offset)
    # for plat in plats:
    #     plat = plat.move(offset, 0)
    #     draw.rect(screen, (0), plat)

    shortcutFunctions.drawSpikes(spikes, offset)
    shortcutFunctions.drawBorders(borders, offset)
    shortcutFunctions.drawTempBird(birds, offset)

    shortcutFunctions.playerSprites(player, p, sprites, vPlayer)
    hitBox = shortcutFunctions.playerSprites(player, p, sprites, vPlayer)
    draw.rect(screen, (255, 0, 0), [vPlayer[SCREENX], p[Y], hitBox[W], hitBox[H]], 2)

    display.update()
    myClock.tick(60)

def move(p, player, sprites, borders):
    global vPlayer

    shortcutFunctions.playerSprites(player, p, sprites, vPlayer)
    hitBox = shortcutFunctions.playerSprites(player, p, sprites, vPlayer)

    keys = key.get_pressed()

    if keys[K_SPACE]:
        vPlayer[Y] = jumpSpeed

    if keys[K_LEFT]:
        shortcutFunctions.moveGuyLeft(p, player, vPlayer, borders, hitBox)

        # p[ROW] = 3

        # if keys[K_LSHIFT] or keys[K_RSHIFT]:
        #     vPlayer[X] = -10

        # else:
        #     vPlayer[X] = -5

        # if vPlayer[SCREENX] > 350:
        #     vPlayer[SCREENX] -= 5

    elif keys[K_RIGHT]:
        shortcutFunctions.moveGuyRight(p, player, vPlayer, borders, hitBox)

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


def moveBad(player, bird):
    shortcutFunctions.moveBird(player, birds)




def check(p, player, sprites, plats, spikes, borders):
    global vPlayer

    shortcutFunctions.playerSprites(player, p, sprites, vPlayer)
    hitBox = shortcutFunctions.playerSprites(player, p, sprites, vPlayer)

    shortcutFunctions.checkPlats(plats, p, hitBox, vPlayer)
    shortcutFunctions.checkSpikes(p, hitBox, spikes, vPlayer)
    shortcutFunctions.checkBorders(p, hitBox, vPlayer, borders)

    # for plat in plats:
    #     if p[X] + hitBox[W] > plat[X] and p[X] < plat[X] + plat[W] and p[Y] + hitBox[H] <= plat[Y] and p[Y] + hitBox[H] + vPlayer[Y] > plat[Y]:
    #         vPlayer[BOT] = plat[Y]
    #         p[Y] = vPlayer[BOT] - hitBox[H]
    #         vPlayer[Y] = 0

    p[Y] += vPlayer[Y]
    player[Y] += vPlayer[Y]

    

    if p[Y] + hitBox[H] >= GROUND:
        vPlayer[BOT] = GROUND
        p[Y] = GROUND - hitBox[H]
        vPlayer[Y] = 0