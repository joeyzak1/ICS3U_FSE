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

jumpSpeed = -20
gravity = 1

GROUND = 575
bottom = GROUND

vPlayer = [0, 0, bottom]

background = image.load('Backgrounds/LevelTwo_backPic.png').convert()
backHeight = background.get_height()

player = [250, 529, 4, 0]

def drawScene(player, sprites):
    global hitBox
    mx, my = mouse.get_pos()
    screen.blit(background, (0, -backHeight + 768))

    shortcutFunctions.playerSprites(player, sprites)
    hitBox = shortcutFunctions.playerSprites(player, sprites)


    myClock.tick(60)
    display.update()
    print ("Ground: 575, Player Hitbox Ground:", hitBox[Y] + hitBox[H])



def move(player, sprites):
    keys = key.get_pressed()

    pRect = Rect(player[X], player[Y], 20, 20)

    if keys[K_SPACE] and vPlayer[Y] == 0 and player[Y] + hitBox[H] >= vPlayer[2]:
        vPlayer[Y] = jumpSpeed
        

    if keys[K_RIGHT] and pRect[X] < 950:
        player[ROW] = 4
        vPlayer[X] = 5


    elif keys[K_LEFT] and pRect[X] > 24:
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

