'''
Joey Zaka and Abbas Zaidi
main.py
ICS3U FSE 
Run this to play the game from start to finish
Multiple modules were used to create the game

ATTENTION TO DETAIL
- Timer will beep on the last 5 seconds
- Sound effect on almost every object in the game
- highlughting rect when hover over in the intro
- Shadow on the timer
- Artwork in photoshop 
- Lives and health shown in corner at all times
- Portion of boss health bar will turn red when you hit the boss
- Tips given throughout the game 
- In the intro, there is a scene PURPOSEFULLY where the player is running without a background
- When you lose health, the game pauses for 100 ms
- The level/intro/game over screen will show on the window bar
- Display Icon
'''

from pygame import *
from shortcutFunctions import *
import os
from importlib import * #ONLY WORKS FOR PYTHON 3.4 AND ABOVE - for when health goes down to zero, reload the entire module (found from https://www.geeksforgeeks.org/reloading-modules-python/)
'''IF YOU ARE USING PYTHON VERSION LESS THAN 3.4 (NOT 2), PLEASE COMMENT PREVIOUS LINE AND UNCOMMENT NEXT LINE'''
# from imp import *
'''IF YOU ARE USING PYTHON VERSION 2.x, UNCOMMENT BOTH IMPORTLIB AND IMP, nothing is needed'''
import intro #intro.py
import levelOne #levelOne.py
import levelTwo as lev2
import levelThree as lv3
import boss as bs
import outro
import sys #for quitting pygame window without going to previous

bh=False
os.environ['SDL_VIDEO_WINDOW_POS'] = "825,525"  # to position pygame window

init()
width, height = 1024, 768; screen = display.set_mode((width,height))
 
RED = (255,0,0); GREY = (127,127,127); BLACK = (0,0,0); WHITE = (255,255,255); BLUE = (0,0,255); GREEN = (0,255,0); YELLOW = (255,255,0) #cols

running = True; myClock = time.Clock() #pg stuff

moveBackground = 0; moveWalking = 0
second = False #to know if the game is being played for the second time

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
    
ch1_intro = [0, 646, 4, 0] #ch1 location and sprite list for 
ch1_levelOne = [512, 675, 4, 0]
p = Rect(512, 675, 35, 50) #beginning rect for level one
bullets_slugs = []
currentScene = ''


def addBossSprites(name, start, end):
    'this function adds sprites to a list which is then added to another list of sprites'
    boss_sprites = [image.load("Sprites/Boss/%s%03d.png" %(name, i)) for i in range(start, end+1)] #adding all the sprites required using list comprehension
    return boss_sprites #return a list of sprites

bossSprites = [] #boss sprites list
bossSprites.append(addBossSprites("tile", 0, 0)) #idle
bossSprites.append(addBossSprites("tile", 4, 5)) #other
bossSprites.append(addBossSprites("tile", 8, 10)) #attack
bossSprites.append(addBossSprites("tile", 12, 15)) #right
bossSprites.append(addBossSprites("tile", 16, 19)) #left

for i in range(len(bossSprites)): #go through boss sprites and change size of each sprite to 300 by 272
    for j in range(len(bossSprites[i])):
        bossSprites[i][j] = transform.scale(bossSprites[i][j], (300, 272))

timeFont = font.Font('fonts/Freshman.ttf', 40) #font for time in corner

display.set_icon(ch1_sprites[4][0])

health_img = [image.load("Health/Health="+str(i)+".png") for i in range(1, 4)] #health images
lives = 5 #amount of lives


def menu(action, p, lives):
    'main menu'
    global second
    while action == 'menu':
        for evt in event.get():
            if evt.type == QUIT:
                sys.exit()
                quit()


        mx, my = mouse.get_pos(); mb = mouse.get_pressed()
        if second: #checking if its not the first time going through the game starting at the intro
            reload(outro) #reload all modules
            reload(levelOne)
            reload(lev2)
            reload(lv3)
            reload(bs)
            p = Rect(512, 675, 35, 50) #player rect for level 1
            lives = 5 #reset lives
            second = False #set to false

        '''Every single function will follow the same format'''

        intro.move_intro(ch1_intro, ch1_sprites, moveBackground, moveWalking)
        intro.helpDialog, intro.timePassed, intro.timeCounter = intro.draw_introScene(ch1_intro, ch1_sprites, moveBackground, moveWalking, intro.helpDialog, intro.timePassed, intro.timeCounter)

        if intro.timeCounter == 95 and not second: #checking if the intro screen isnt black anymore and can play music
            mixer.music.load('audio/IntroBack.wav') #load the music and play it
            mixer.music.play(-1)



        if mb[0] == 1 and intro.introRects[0].collidepoint(mx, my) and len(intro.timePassed) > 2: #check if new game was clicked, go to level one
            mixer.music.load('audio/lev1Back.wav') #play level one music
            mixer.music.play(-1) #loop the music
            level_One('lev1', p, lives)
        


def level_One(action, p, lives):
    'level one'
    while action == 'lev1':
        for evt in event.get():
            if evt.type == QUIT:
                sys.exit()
                quit()

        if levelOne.check_levelTwo(levelOne.doorRect, p):
            mixer.music.load('audio/lev2Back.wav')
            mixer.music.play(-1)
            level_Two('lev2', lev2.pRect, lives) #checking if enetered door at end

        else:
            if levelOne.health < 0 or len(levelOne.timePassed) == 125: #checking if health goes below zero (DEAD)
                p = Rect(512, 675, 35, 50) #beginning rect for level one 
                health = 2 #reset health
                lives -= 1 #lower lives by 1
                if lives == -1: #checking if lives go below 0
                    mixer.music.load('audio/gameOverAudio.wav') #load gane over music
                    mixer.music.play(-1) #play it
                    gameOver('over', lives) #play game over scene
                reload(levelOne) #if all health is taken away, restart the level

            else: #normal game loop
                levelOne.v = levelOne.move(p, ch1_levelOne, ch1_sprites, levelOne.blocks, levelOne.birds, levelOne.borders, levelOne.v)
                levelOne.move_bird(p, levelOne.birds, levelOne.bird_p, bird_sprites)
                levelOne.isJump = levelOne.check(p, ch1_levelOne, ch1_sprites,levelOne.v,levelOne.plats, levelOne.slugs, levelOne.borders, levelOne.bird_p, levelOne.doorRect, levelOne.healthSq, levelOne.timePassed, levelOne.isJump)
                levelOne.timePassed, levelOne.myCounter = levelOne.drawScene(screen, p, ch1_sprites, ch1_levelOne, levelOne.plats, levelOne.blocks, 
                    levelOne.squared_blocks, levelOne.slugs, bullets_slugs, levelOne.birds, levelOne.bird_p, bird_sprites, levelOne.borders, 
                    levelOne.doorRect, health_img, levelOne.health, timeFont, lives, levelOne.timePassed, levelOne.myCounter, levelOne.v)


        

def level_Two(action, p, lives):
    'level two'
    # global lives
    while action == 'lev2':
        for evt in event.get():
            if evt.type == QUIT:
                sys.exit()
                quit()

            
        if checkDoor(lev2.pRect, lev2.doorRect): #checking if enetered door for level 3, goes to level 3
            mixer.music.load('audio/lev3Back.wav')
            mixer.music.play(-1)
            level_Three('lev3', lv3.pRect, lives)

        else:
            if lev2.health < 0 or len(lev2.timePassed) == 300: #checking if player died, see comments for lev 1 (same process)
                p = Rect(250, 529, 4, 0) #resetting a few things
                lev2.health = 2
                lives -= 1
                if lives == -1:
                    mixer.music.load('audio/gameOverAudio.wav')
                    mixer.music.play(-1)
                    gameOver('over', lives)
                reload(lev2) #restart level 2

            else: #normal game loop
                lev2.vPlayer = lev2.move(lev2.pRect, lev2.player, ch1_sprites, lev2.borders, lev2.spikes, lev2.vPlayer)
                lev2.moveBad(lev2.player, lev2.birds)
                lev2.health = lev2.check(lev2.pRect, lev2.player, ch1_sprites, lev2.plats, lev2.spikes, lev2.borders, lev2.healthBlocks, health_img, lev2.birds, lev2.timePassed, lev2.vPlayer, lev2.health)
                lev2.timePassed, lev2.myCounter = lev2.drawScene(lev2.pRect, lev2.player, ch1_sprites, lev2.plats, lev2.platPic, lev2.spikes, lev2.borders, lev2.birds, bird_sprites, 
                lev2.healthBlocks, health_img, lev2.doorRect, timeFont, lives, lev2.vPlayer, lev2.health, lev2.timePassed, lev2.myCounter)

        


def level_Three(action, p, lives):
    'level three'
    while action == 'lev3':
        for evt in event.get():
            if evt.type == QUIT:
                sys.exit()
                quit()


        if lv3.checkBoss(lv3.pRect, lv3.doorRect): #goes to boss if door was clicked
            mixer.music.load('audio/bossBack.wav') #plays boss music
            mixer.music.play(-1)
            boss('boss', lives) #boss

        else: #game loop
            lv3.v = lv3.move(lv3.pRect, lv3.player, ch1_sprites, lv3.v)
            lv3.check(lv3.pRect, lv3.player, ch1_sprites, lv3.v)
            lv3.drawScene(lv3.pRect, lv3.player, ch1_sprites, lv3.doorRect, lives, health_img, lv3.v)

def boss(action, lives):
    'boss'
    global bh
    while action == 'boss':
        for evt in event.get():
            if evt.type == QUIT:
                sys.exit()
                quit()

        if bs.checkDoor(bs.pRect, bs.door, bs.visible): #checking if the player went into the door after defeating the boss
            mixer.music.load('audio/outroBack.wav') #outro music
            mixer.music.play(-1)
            outro_func('outro', outro.pRect, lives) #outro

        if bs.playerHealth < 0 or len(bs.timePassed) >= 300: #checking if defeated by by boss, same process as others
            for b in bs.timePassed: #remove everything from time passed
                bs.timePassed.remove(b) #reset time
            pRect = Rect(300, 600, 50, 50)
            bs.playerHealth = 2
            reload(lv3) #reload modules
            reload(bs)
            lives -= 1
            if lives == -1:
                mixer.music.load('audio/gameOverAudio.wav')
                mixer.music.play(-1)
                gameOver('over', lives)
            mixer.music.load('audio/lev3Back.wav')
            mixer.music.play(-1)
            level_Three('lev3', pRect, lives) #go back to lev 3

        else: #normal game loop
            pHealth = bs.mainHealth(bs.playerHealth)
            bs.vPlayer = bs.moveGuy(bs.pRect, bs.player, ch1_sprites, bs.bossRect, bossSprites, timeFont, bs.playerBullets, bs.vPlayer)
            bs.vBoss = bs.moveBoss(bs.boss, bs.bossRect, bs.timePassed, bs.pRect, bossSprites, bs.bossHealth, bs.vBoss)
            if 1: #so the health and bullets will work properly
                bs.bullets,bs.playerHealth,bs.bh, bs.playerBullets, bs.bossHealth, bs.visible, bs.bullSpeed, bs.rapid = bs.checkCollision(
                    bs.pRect, bs.player, ch1_sprites, bs.boss, bs.bossRect, bs.bullets, bs.bossHealth, bs.playerBullets, pHealth, bs.visible, bs.vPlayer, bs.vBoss, bs.bullSpeed, bs.rapid, bs.timePassed)
            bs.myTime, bs.timePassed, bs.timeShown = bs.drawScene(bs.pRect, bs.player, ch1_sprites, bs.boss, bs.bossRect, bs.bullets, bossSprites, timeFont, bs.bossHealth, 
            health_img, bs.playerBullets, pHealth, bs.visible, lives, bs.vPlayer, bs.myTime, bs.timePassed, bs.timeShown)

def outro_func(action, p, lives):
    'outro screen'
    global second
    while action == 'outro':
        for evt in event.get():
            if evt.type == QUIT:
                sys.exit()
                quit()

        if len(outro.timePassed) < 1700:
            outro.drawScene(outro.player, outro.pRect, ch1_sprites, outro.timePassed, outro.myCounter) #only one function for certain amount of time
        
        else: #reset the game after certain amount of time
            reload(intro); reload(levelOne); reload(lev2); reload(lv3); reload(bs); reload(outro)
            ch1_intro = [0, 646, 4, 0] #ch1 location and sprite list for 
            second = True
            menu('menu', ch1_intro, lives)

timePassed = [] #time passed
myCounter = 0 #counter

gameOverImg = image.load('Other/GameOverScreen.png').convert() #game over image

def gameOver(action, lives): #game over screen
    global myCounter
    global timePassed
    global second

    while action == 'over':
        for evt in event.get():
            if evt.type == QUIT:
                sys.exit()
                quit()
        
        screen.blit(gameOverImg, (0, 0)) #blit the game over image until 10 seconds have passed
        if len(timePassed) == 10: #checking if 10 seconds have passed
            reload(intro) #reload intro module
            second = True #set second = true so all modules can be reloaded in the intro
            mixer.music.load('audio/IntroBack.wav') #load music
            mixer.music.play(-1) #play intro music
            timePassed = []
            myCounter = 0
            menu('menu', p, lives) #run the intro screen

        if myCounter % 60 == 0: #checking if the counter can be divisible by 60
            timePassed.append('t') #append to time list, as 1 second passes each time something is appened
        myCounter += 1 #add one to the counter

        display.set_caption("Super Swordy Boy - GAME OVER     FPS = " + str(int(myClock.get_fps()))) #the title 
        display.update() #update the screen
        myClock.tick(60) #60 fps


menu('menu', p, lives)
quit()
