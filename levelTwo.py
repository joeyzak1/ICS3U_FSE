#levelTwo.py

from pygame import *

screen = display.set_mode((1024, 768))
myClock = time.Clock()

X = 0
Y = 1
W = 2
H = 3

GROUND = 600
bottom = GROUND

vPlayer = [0, 0, bottom]

background = image.load('Backgrounds/LevelTwo_backPic.png').convert()
backHeight = background.get_height()

player = [250, 600, 4, 0]

def drawScene(player):
    # screen.fill((0))
    pRect = Rect(player[X], player[Y], 20, 20)
    screen.blit(background, ((background.get_height()-600), 0))
    draw.rect(screen, (255, 0, 0), pRect)
    myClock.tick(60)
    display.update()



def move(player, sprites):
    keys = key.get_pressed()

    pRect = Rect(player[X], player[Y], 20, 20)

    if keys[K_RIGHT]:
        vPlayer[X] += 5

    elif keys[K_LEFT]:
        vPlayer[X] -= 5

    else:
        vPlayer[X] = 0

    player[X] += vPlayer[X]