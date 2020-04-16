'''
main.py
ICS3U FSE

Run this file to play the game

'''
from pygame import *
import intro #intro.py
import levelOne #levelOne.py

init()
width, height = 1024, 768; screen = display.set_mode((width,height))

RED = (255,0,0); GREY = (127,127,127); BLACK = (0,0,0); WHITE = (255,255,255); BLUE = (0,0,255); GREEN = (0,255,0); YELLOW = (255,255,0)

running = True; myClock = time.Clock()

moveBackground = 0; moveWalking = 0


#ADDING SPRITES -----------------------------------------------------------------------------------
def add_ch1_sprites(name, start, end):
    my_ch1Sprites = [image.load("Sprites/Character1/%s%03d.png" %(name, i)) for i in range(start, end+1)] #adding all the sprites required using list comprehension
    return my_ch1Sprites

ch1_sprites = [] #2d list
ch1_sprites.append(add_ch1_sprites("Ch1_", 0, 4)); ch1_sprites.append(add_ch1_sprites("Ch1_", 5, 9)); ch1_sprites.append(add_ch1_sprites("Ch1_", 10, 15))
ch1_sprites.append(add_ch1_sprites("Ch1_", 16, 28)); ch1_sprites.append(add_ch1_sprites("Ch1_", 29, 41))

X = 0; Y = 1; ROW = 2; COL = 3 #for navigation in lists

ch1_intro = [0, 500, 4, 0] #ch1 location and sprite list for 
p = Rect(512, 675, 35, 50) #beginning rect for level one

#true or false variables for starting and ending certain functions
introRun = True
levelOne_Run = False


while running:
    for evt in event.get():
        if evt.type == QUIT:
            running=False
                       
    mx, my = mouse.get_pos(); mb = mouse.get_pressed(); keys = key.get_pressed()

    if introRun: #intro scene
        intro.move_intro(ch1_intro, ch1_sprites, moveBackground, moveWalking)
        intro.draw_introScene(ch1_intro, ch1_sprites, moveBackground, moveWalking)
        if mb[0] == 1 and intro.introRects[0].collidepoint(mx, my):
            introRun = False
            levelOne_Run = True

    elif levelOne_Run: #level one
        levelOne.move(p)
        levelOne.check(p)
        levelOne.drawScene(screen, p)

    print (introRun, levelOne_Run)
      

    display.set_caption(str(int(myClock.get_fps())))
    myClock.tick(60) #60 fps
    display.update()
            
quit()
