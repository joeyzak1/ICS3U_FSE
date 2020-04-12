'''
main.py
ICS3U FSE

Run this file to play the game

'''
from pygame import *
import intro

init()
width, height = 1024, 768
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


#ADDING SPRITES -----------------------------------------------------------------------------------
def add_ch1_sprites(name, start, end):
    my_ch1Sprites = []
    for i in range(start, end+1):
        my_ch1Sprites.append(image.load("Sprites/Character1/%s%03d.png" %(name, i)))

    return my_ch1Sprites

ch1_sprites = [] #2d list
ch1_sprites.append(add_ch1_sprites("Ch1_", 0, 4))
ch1_sprites.append(add_ch1_sprites("Ch1_", 5, 9))
ch1_sprites.append(add_ch1_sprites("Ch1_", 10, 15))
ch1_sprites.append(add_ch1_sprites("Ch1_", 16, 28))
ch1_sprites.append(add_ch1_sprites("Ch1_", 29, 41))

X = 0
Y = 1
ROW = 0
COL = 4


ch1 = [50, 500, 0, 4]


while running:
    for evt in event.get():
        if evt.type == QUIT:
            running=False
                       
    mx, my = mouse.get_pos()
    mb = mouse.get_pressed()
    keys = key.get_pressed()

    intro.move_player(ch1)
    intro.draw_intro(screen, ch1, ch1_sprites)
      
   
    myClock.tick(60) #60 fps
    display.flip()
            
quit()
