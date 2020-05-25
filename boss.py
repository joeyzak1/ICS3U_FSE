#boss.py

from pygame import *
import shortcutFunctions

screen = display.set_mode((1024, 768))
myClock = time.Clock()


def drawScene():
    screen.fill((0))
    display.update()
    myClock.tick(60)

def moveGuy():
    keys = key.get_pressed()

def moveBoss():
    screen.fill((0))

def checkCollision():
    keys = key.get_pressed()