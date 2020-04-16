'''
main.py
ICS3U FSE

Run this file to play the game

'''
from pygame import *
import intro

init()
width, height = 1024, 768; screen = display.set_mode((width,height))

RED = (255,0,0); GREY = (127,127,127); BLACK = (0,0,0); WHITE = (255,255,255); BLUE = (0,0,255); GREEN = (0,255,0); YELLOW = (255,255,0)

running = True; myClock = time.Clock()

moveBackground = 0; moveWalking = 0


#ADDING SPRITES -----------------------------------------------------------------------------------
def add_ch1_sprites(name, start, end):
    my_ch1Sprites = [image.load("Sprites/Character1/%s%03d.png" %(name, i)) for i in range(start, end+1)]
##    for i in range(start, end+1):
##        my_ch1Sprites.append(image.load("Sprites/Character1/%s%03d.png" %(name, i)))

    return my_ch1Sprites

ch1_sprites = [] #2d list
ch1_sprites.append(add_ch1_sprites("Ch1_", 0, 4)); ch1_sprites.append(add_ch1_sprites("Ch1_", 5, 9)); ch1_sprites.append(add_ch1_sprites("Ch1_", 10, 15))
ch1_sprites.append(add_ch1_sprites("Ch1_", 16, 28)); ch1_sprites.append(add_ch1_sprites("Ch1_", 29, 41))

X = 0; Y = 1; ROW = 2; COL = 3


ch1 = [0, 500, 4, 0]

introRun = True


while running:
    for evt in event.get():
        if evt.type == QUIT:
            running=False
                       
    mx, my = mouse.get_pos(); mb = mouse.get_pressed(); keys = key.get_pressed()

    if introRun == True:
        intro.move_intro(ch1, ch1_sprites, moveBackground, moveWalking)
        intro.draw_introScene(ch1, ch1_sprites, moveBackground, moveWalking)
      

    display.set_caption(str(int(myClock.get_fps())))
    myClock.tick(60) #60 fps
    display.update()
            
quit()
