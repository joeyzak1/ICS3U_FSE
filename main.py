'''
main.py
ICS3U FSE 
Run this to play the game from start to finish
'''

from pygame import *
import intro #intro.py
import levelOne #levelOne.py

init()
width, height = 1024, 768; screen = display.set_mode((width,height))

RED = (255,0,0); GREY = (127,127,127); BLACK = (0,0,0); WHITE = (255,255,255); BLUE = (0,0,255); GREEN = (0,255,0); YELLOW = (255,255,0) #cols

running = True; myClock = time.Clock() #pg stuff

moveBackground = 0; moveWalking = 0


#ADDING SPRITES -----------------------------------------------------------------------------------
def add_ch1_sprites(name, start, end):
    my_ch1Sprites = [image.load("Sprites/Character1/%s%03d.png" %(name, i)) for i in range(start, end+1)] #adding all the sprites required using list comprehension
    return my_ch1Sprites

ch1_sprites = [] #2d list
ch1_sprites.append(add_ch1_sprites("Ch1_", 0, 4)); ch1_sprites.append(add_ch1_sprites("Ch1_", 5, 9)); ch1_sprites.append(add_ch1_sprites("Ch1_", 10, 15))
ch1_sprites.append(add_ch1_sprites("Ch1_", 16, 28)); ch1_sprites.append(add_ch1_sprites("Ch1_", 29, 41))

X = 0; Y = 1; ROW = 2; COL = 3 #for navigation in lists

ch1_intro = [0, 646, 4, 0] #ch1 location and sprite list for 
ch1_levelOne = [512, 675, 4, 0]
p = Rect(512, 675, 35, 50) #beginning rect for level one
bullets_slugs = []


#true or false variables for starting and ending certain functions
introRun = True
levelOne_Run = False
display.set_icon(ch1_sprites[4][0])



def menu(action):
    while action == 'menu':
        for evt in event.get():
            if evt.type == QUIT:
                action = 'end'

        mx, my = mouse.get_pos(); mb = mouse.get_pressed()

        intro.move_intro(ch1_intro, ch1_sprites, moveBackground, moveWalking)
        intro.draw_introScene(ch1_intro, ch1_sprites, moveBackground, moveWalking)

        if mb[0] == 1 and intro.introRects[0].collidepoint(mx, my):
            # action = 'lev1'
            level_One('lev1')

        display.set_caption("Super Swordy Boy - Intro Screen     FPS = " + str(int(myClock.get_fps())))
        display.update()
        myClock.tick(60)

def level_One(action):
    while action == 'lev1':
        for evt in event.get():
            if evt.type == QUIT:
                action = 'end'


        levelOne.move(p, ch1_levelOne, ch1_sprites)
        levelOne.move_slugBullets(bullets_slugs)
        levelOne.check(p, levelOne.plats)
        levelOne.check_bullSlug(bullets_slugs, p)
        levelOne.drawScene(screen, p, ch1_sprites, ch1_levelOne, levelOne.plats, levelOne.blocks, levelOne.squared_blocks, levelOne.slugs, bullets_slugs, levelOne.birds)


        display.set_caption("Super Swordy Boy - Level One     FPS = " + str(int(myClock.get_fps())))
        display.update()
        myClock.tick(60)



menu('menu')
quit()


