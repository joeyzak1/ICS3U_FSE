'''
main.py
ICS3U FSE

Run this file to play the game

'''
from pygame import *

init()
width, height = 800, 600
screen = display.set_mode((width,height))

RED = (255,0,0)
GREY = (127,127,127)
BLACK = (0,0,0)
WHITE = (255,255,255)
BLUE = (0,0,255)
GREEN = (0,255,0)
YELLOW = (255,255,0)

running = True
myClock = time.Clock()





while running:
    for evt in event.get():
        if evt.type == QUIT:
            running=False
                       
    mx, my = mouse.get_pos()
    mb = mouse.get_pressed()
    keys = key.get_pressed()
      
   
    myClock.tick(60) #60 fps
    display.flip()
            
quit()