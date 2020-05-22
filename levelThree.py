#levelThree.py
'''
this part of the program is just the part where you walk to the boss portion, no other obstacles
'''

from pygame import *
import shortcutFunctions

screen = display.set_mode((1024, 768))
myClock = time.Clock()

def drawScene():
    screen.fill((0))

    myClock.tick(60)
    display.update()

def move():
    keys = key.get_pressed()