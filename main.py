'''
main.py
ICS3U FSE 
Run this to play the game from start to finish
'''

from pygame import *
from shortcutFunctions import *
import os
import intro #intro.py
import levelOne #levelOne.py
import newLevelTwo as lev2

os.environ['SDL_VIDEO_WINDOW_POS'] = "825,525"  # to position pygame window

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

bird_images = ['Sprites/Bird/tile00' + str(i) + '.png' for i in range (5)]
bird_sprites = []
for i in bird_images:
    i = image.load(i)
    i = transform.scale(i, (100, 80))
    bird_sprites.append(i)
    

# X = 0; Y = 1; ROW = 2; COL = 3 #for navigation in lists

ch1_intro = [0, 646, 4, 0] #ch1 location and sprite list for 
ch1_levelOne = [512, 675, 4, 0]
p = Rect(512, 675, 35, 50) #beginning rect for level one
bullets_slugs = []


#true or false variables for starting and ending certain functions
# introRun = True
# levelOne_Run = False
display.set_icon(ch1_sprites[4][0])

health_img = [image.load("Health/Health="+str(i)+".png") for i in range(1, 4)]

def get_hitbox(pic, size):
    pic_w = pic.get_width()
    pic_h = pic.get_height()

    hitbox = Rect(size[X], size[Y], pic_w, pic_h)
    return hitbox




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
            screen.fill((0))
            level_Two('lev2')

        


def level_One(action):
    while action == 'lev1':
        for evt in event.get():
            if evt.type == QUIT:
                action = 'end'


        # levelOne.move(p, ch1_levelOne, ch1_sprites, levelOne.blocks, levelOne.birds)
        # levelOne.move_bad(p, bullets_slugs, levelOne.birds, levelOne.bird_p, bird_sprites)
        # # levelOne.move_slugBullets(bullets_slugs)
        # levelOne.check(p, ch1_levelOne, ch1_sprites,levelOne.pHitbox,levelOne.plats, levelOne.slugs, levelOne.borders, levelOne.bird_p, levelOne.bird_hitboxes, levelOne.doorRect, levelOne.healthSq)
        # levelOne.check_bullSlug(bullets_slugs, p)

        if levelOne.check_levelTwo(levelOne.doorRect, p):
            level_Two('lev2')

        else:
            levelOne.move(p, ch1_levelOne, ch1_sprites, levelOne.blocks, levelOne.birds)
            levelOne.move_bad(p, bullets_slugs, levelOne.birds, levelOne.bird_p, bird_sprites)
            # levelOne.move_slugBullets(bullets_slugs)
            levelOne.check(p, ch1_levelOne, ch1_sprites,levelOne.pHitbox,levelOne.plats, levelOne.slugs, levelOne.borders, levelOne.bird_p, levelOne.bird_hitboxes, levelOne.doorRect, levelOne.healthSq)
            levelOne.check_bullSlug(bullets_slugs, p)
            levelOne.drawScene(screen, p, ch1_sprites, ch1_levelOne, levelOne.plats, levelOne.blocks, 
                levelOne.squared_blocks, levelOne.slugs, bullets_slugs, levelOne.birds, levelOne.bird_p, bird_sprites, levelOne.borders, 
                levelOne.doorRect, health_img, levelOne.health)


        


def level_Two(action):
    while action == 'lev2':
        for evt in event.get():
            if evt.type == QUIT:
                action = 'end'

        lev2.move(lev2.player, ch1_sprites)
        lev2.moveBad(lev2.player, lev2.birds)
        lev2.check(lev2.player, ch1_sprites, lev2.plats)
        lev2.drawScene(lev2.player, ch1_sprites, lev2.plats, lev2.spikes, lev2.borders, lev2.birds)


        display.set_caption("Super Swordy Boy - Level Two     FPS = " + str(int(myClock.get_fps())))
        display.update()
        myClock.tick(60)




menu('menu')
quit()