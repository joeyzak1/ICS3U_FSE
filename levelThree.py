#levelThree.py
'''
this part of the program is just the part where you walk to the boss portion, no other obstacles
'''

from pygame import *
import shortcutFunctions

screen = display.set_mode((1024, 768))
myClock = time.Clock()

player = [50, 600, 4, 0]
pRect = Rect(50, 600, 50, 50)

def drawScene():
    screen.fill((0))

    myClock.tick(60)
    display.update()

def move():
    keys = key.get_pressed()