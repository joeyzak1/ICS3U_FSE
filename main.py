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
import levelThree as lv3
import boss as bs


os.environ['SDL_VIDEO_WINDOW_POS'] = "825,525"  # to position pygame window

init()
width, height = 1024, 768; screen = display.set_mode((width,height))
music = ['audio/RunningSoundEffectIntro.ogg', 'audio/MainMenuMusic.ogg']
music_pos = 0

RED = (255,0,0); GREY = (127,127,127); BLACK = (0,0,0); WHITE = (255,255,255); BLUE = (0,0,255); GREEN = (0,255,0); YELLOW = (255,255,0) #cols

running = True; myClock = time.Clock() #pg stuff

moveBackground = 0; moveWalking = 0


#ADDING SPRITES -----------------------------------------------------------------------------------
def add_ch1_sprites(name, start, end):
    my_ch1Sprites = [image.load("Sprites/Character1/%s%03d.png" %(name, i)) for i in range(start, end+1)] #adding all the sprites required using list comprehension
    return my_ch1Sprites #return a list of sprites

ch1_sprites = [] #2d list of sprites
#adding all the sprites as seperate lists
ch1_sprites.append(add_ch1_sprites("Ch1_", 0, 4)); ch1_sprites.append(add_ch1_sprites("Ch1_", 5, 9)); ch1_sprites.append(add_ch1_sprites("Ch1_", 10, 15))
ch1_sprites.append(add_ch1_sprites("Ch1_", 16, 28)); ch1_sprites.append(add_ch1_sprites("Ch1_", 29, 41))

bird_images = ['Sprites/Bird/tile00' + str(i) + '.png' for i in range (5)] #getting all the bird sprites
bird_sprites = [] #for loaded
for i in bird_images: #going through the pictures
    i = image.load(i)
    i = transform.scale(i, (100, 80)) #resize to 100 by 80
    bird_sprites.append(i) #add to sprite list
    

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




def menu(action, m):
    while action == 'menu':
        for evt in event.get():
            if evt.type == QUIT:
                action = 'end'

        # mixer.music.load(intro.music[intro.m])
        # mixer.music.play(-1)


        mx, my = mouse.get_pos(); mb = mouse.get_pressed()

        intro.move_intro(ch1_intro, ch1_sprites, moveBackground, moveWalking)
        intro.draw_introScene(ch1_intro, ch1_sprites, moveBackground, moveWalking)



        if mb[0] == 1 and intro.introRects[0].collidepoint(mx, my):
            # action = 'lev1'
            level_One('lev1', m)
            # level_Three('lev3')
            # boss('boss')

        


def level_One(action, m):
    while action == 'lev1':
        for evt in event.get():
            if evt.type == QUIT:
                action = 'end'

        m = 1
        if levelOne.check_levelTwo(levelOne.doorRect, p):
            level_Two('lev2', m)

        else:
            levelOne.move(p, ch1_levelOne, ch1_sprites, levelOne.blocks, levelOne.birds)
            levelOne.move_bad(p, bullets_slugs, levelOne.birds, levelOne.bird_p, bird_sprites)
            # levelOne.move_slugBullets(bullets_slugs)
            levelOne.check(p, ch1_levelOne, ch1_sprites,levelOne.pHitbox,levelOne.plats, levelOne.slugs, levelOne.borders, levelOne.bird_p, levelOne.bird_hitboxes, levelOne.doorRect, levelOne.healthSq)
            levelOne.check_bullSlug(bullets_slugs, p)
            levelOne.drawScene(screen, p, ch1_sprites, ch1_levelOne, levelOne.plats, levelOne.blocks, 
                levelOne.squared_blocks, levelOne.slugs, bullets_slugs, levelOne.birds, levelOne.bird_p, bird_sprites, levelOne.borders, 
                levelOne.doorRect, health_img, levelOne.health)


        

def level_Two(action, m):
    while action == 'lev2':
        for evt in event.get():
            if evt.type == QUIT:
                action = 'end'
            
        m = 2
        if checkDoor(lev2.pRect, lev2.doorRect):
            level_Three('lev3', m)

        else:
            lev2.move(lev2.pRect, lev2.player, ch1_sprites, lev2.borders, lev2.spikes)
            lev2.moveBad(lev2.player, lev2.birds)
            lev2.check(lev2.pRect, lev2.player, ch1_sprites, lev2.plats, lev2.spikes, lev2.borders, health_img, lev2.birds)
            lev2.drawScene(lev2.pRect, lev2.player, ch1_sprites, lev2.plats, lev2.platPic, lev2.spikes, lev2.borders, lev2.birds, bird_sprites, lev2.healthBlocks, health_img, lev2.doorRect)


        


def level_Three(action, m):
    while action == 'lev3':
        for evt in event.get():
            if evt.type == QUIT:
                action = 'end'

        m = 3

        if lv3.checkBoss(lv3.pRect, lv3.doorRect):
            boss('boss', m)

        else:
            lv3.move(lv3.pRect, lv3.player, ch1_sprites)
            lv3.drawScene(lv3.pRect, lv3.player, ch1_sprites, lv3.doorRect)

def boss(action, m):
    while action == 'boss':
        for evt in event.get():
            if evt.type == QUIT:
                action = 'end'

        m = 4

        bs.moveGuy(bs.pRect, bs.player, ch1_sprites, bs.bossRect)
        bs.moveBoss(bs.boss, bs.bossRect, bs.timePassed, bs.pRect)
        bs.checkCollision(bs.pRect, bs.player, ch1_sprites, bs.boss, bs.bossRect, bs.bullets)
        bs.drawScene(bs.pRect, bs.player, ch1_sprites, bs.boss, bs.bossRect, bs.bullets)
        
# playMusic(music, music_pos)


menu('menu', music_pos)
quit()