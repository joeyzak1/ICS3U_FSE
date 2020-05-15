from pygame import *
import shortcutFunctions

init()
myClock = time.Clock()
screen = display.set_mode((1024, 768))

X = 0
Y = 1
W = 2
H = 3
ROW = 2
COL = 3
BOT = 2

jumpSpeed = -20
gravity = 1

GROUND = 574
bottom = GROUND

moveBack = 0

vPlayer = [0, 0, bottom]

background = image.load('Backgrounds/LevelTwo_backPic.png').convert()
backHeight = background.get_height()
backWidth = background.get_width()
backRect = Rect(0, 0, backWidth, backHeight)

player = [250, 529, 4, 0]

plats = [Rect(700, 400, 200, 15), Rect(450, 300, 200, 15), Rect(50, 200, 200, 15)]
# plats = [Rect(900, 525, 200, 15), Rect(3000, 460, 200, 15), Rect(5000, 530, 200, 15), Rect(5400, 450, 200, 15), Rect(6300, 525, 200, 15),
#         Rect(6600, 400, 200, 15), Rect(6900, 275, 200, 15)]

EVERYTHING = []

def drawScene(player, sprites, plats):
    global backRect

    mx, my = mouse.get_pos()

    backRect = backRect.move(0, moveBack)
    screen.blit(background, (0, -backRect[Y] - backHeight + 768 ))

    shortcutFunctions.drawPlats (plats, moveBack)

    shortcutFunctions.playerSprites(player, sprites)
    hitBox = shortcutFunctions.playerSprites(player, sprites)

    draw.rect(screen, (255, 0, 0), hitBox, 2)

    myClock.tick(60)
    display.update()
    

def move(player, sprites):
    global vPlayer
    global moveBack

    keys = key.get_pressed()

    hitBox = shortcutFunctions.playerSprites(player, sprites)

    # pRect = Rect(player[X], player[Y], 20, 20)

    if keys[K_SPACE] and player[Y] + hitBox[H] == vPlayer[BOT] and vPlayer[Y] == 0:
        vPlayer[Y] = jumpSpeed
        

    if keys[K_RIGHT] and player[X] < 950:
        player[ROW] = 4
        vPlayer[X] = 5


    elif keys[K_LEFT] and player[X] > 24:
        player[ROW] = 3
        vPlayer[X] = -5

    else:
        player[COL] = 0
        player[COL] -= 0.2
        vPlayer[X] = 0

    player[COL] += 0.2

    if player[COL] >= len(sprites[ROW]):
        player[COL] = 1

    player[X] += vPlayer[X]
    vPlayer[Y] += gravity
    moveBack -= 0.5


def check(player, sprites, plats):
    global vPlayer
    global GROUND

    print (vPlayer[BOT])

    keys = key.get_pressed()

    hitBox = shortcutFunctions.playerSprites(player, sprites)
    p = Rect(player[X], player[Y], hitBox[W], hitBox[H])

    player[Y] += vPlayer[Y]
    # vPlayer[BOT] += int(moveBack)

    shortcutFunctions.checkPlats(plats, player, hitBox, vPlayer, moveBack)


    if vPlayer[Y] == 0 and player[Y] + hitBox[H] == vPlayer[BOT]:
        player[Y] == vPlayer[BOT] - hitBox[H]


    if player[Y] + hitBox[H] >= GROUND + int(moveBack):
        vPlayer[BOT] = GROUND + int(moveBack)
        player[Y] = (GROUND + int(moveBack)) - hitBox[H]
        # player[Y] += int(moveBack)
        if keys[K_SPACE]:
            vPlayer[Y] = jumpSpeed
        else:
            vPlayer[Y] = 0

    # shortcutFunctions.checkPlats(player, hitBox, vPlayer, plats)