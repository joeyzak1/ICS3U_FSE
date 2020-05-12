#levelTwo.py

from pygame import *
import shortcutFunctions

init()

screen = display.set_mode((1024, 768))
myClock = time.Clock()

X = 0
Y = 1
W = 2; ROW = 2; BOT = 2
H = 3; COL = 3

jumpSpeed = -21
gravity = 1

GROUND = 574
bottom = GROUND

vPlayer = [0, 0, bottom]

moveBackground = 0

background = image.load('Backgrounds/LevelTwo_backPic.png').convert()
backHeight = background.get_height()

player = [250, 529, 4, 0]
hitList = []

plats = [Rect(700, 400, 200, 15)]

def drawScene(player, sprites, plats):
    global moveBackground

    mx, my = mouse.get_pos()
    screen.blit(background, (0, -backHeight + int(moveBackground) + 768))

    shortcutFunctions.drawPlats (plats, moveBackground)

    shortcutFunctions.playerSprites(player, sprites)
    hitBox = shortcutFunctions.playerSprites(player, sprites)
    # addList(hitBox)
    draw.rect(screen, (255, 0, 0), hitBox, 2)
    draw.line (screen, (255, 0, 0), (0, vPlayer[BOT] + moveBackground), (1024, vPlayer[BOT] + moveBackground), 3) #ground line


    myClock.tick(60)
    display.update()
    moveBackground += 0.5
    

    # print ("Ground: 575, Player Hitbox Ground:", hitBox[Y] + hitBox[H])



def move(player, sprites):
    keys = key.get_pressed()

    shortcutFunctions.playerSprites(player, sprites)
    hitBox = shortcutFunctions.playerSprites(player, sprites)

    # pRect = Rect(player[X], player[Y], 20, 20)

    if keys[K_SPACE] and hitBox[Y] + hitBox[H] == vPlayer[BOT] and vPlayer[Y] == 0:
        print ('jump')
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

    print(vPlayer[Y])
    vPlayer[BOT] += int(moveBackground)

def check(player, sprites):
    global moveBackground

    shortcutFunctions.playerSprites(player, sprites)
    hitBox = shortcutFunctions.playerSprites(player, sprites)

    # playerRect = Rect(player[X], player[Y], hitBox[W], hitBox[H])

    # if 573 < (playerRect[Y] + playerRect[H]) < 578:
    #     player[Y] = GROUND - hitBox[H]

    player[Y] += vPlayer[Y]

    if hitBox[Y] + hitBox[H] == vPlayer[BOT]:
        player[Y] = vPlayer[BOT] - hitBox[H] + int(moveBackground)

    if hitBox[Y] + hitBox[H] >= GROUND:
        vPlayer[BOT] = GROUND
        player[Y] = GROUND - hitBox[H] + int(moveBackground)
        vPlayer[Y] = 0

def addList(hitbox):
    hitList.append(hitbox)
