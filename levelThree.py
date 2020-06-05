#levelThree.py
'''
this part of the program is just the part where you walk to the boss portion, no other obstacles
'''

from pygame import *
import shortcutFunctions

screen = display.set_mode((1024, 768)) 
myClock = time.Clock()

#navigation variables
X = 0
Y = 1
W = 2
H = 3
ROW = 2
COL = 3
BOT = 2
SCREENX = 3

#required picture (background and lives)
backPic = image.load('Backgrounds/LevelThree_BackPic.png').convert()
livesPic = image.load('Other/live.png')

#GROUND AND BOTTOM FOR VEL
GROUND = 633
bottom = GROUND

#vel and jumping
v = [0, 0, bottom, 50]
jumpSpeed = -20
gravity = 1

#player
player = [300, 600, 4, 0]
pRect = Rect(300, 600, 50, 50)

#rect object for door
doorRect = Rect(3100, 300, 300, GROUND-300)

#sound effects
jumpSound = mixer.Sound('audio/effects/Jump.wav')
movement = mixer.Sound('audio/effects/movement.wav')
movement.set_volume(.05)
bossDoor = mixer.Sound('audio/Effects/bossDoor.wav')
sword = mixer.Sound('audio/effects/sword.wav')

def drawScene(p, player, sprites, doorRect, lives, healthPic, v):
    'draws the scene'

    offset = v[SCREENX] - p[X] #offset
    screen.blit(backPic, (offset, 0)) #draw the background according to the offset

    doorRect = doorRect.move(offset, 0) #move the door

    hitbox = shortcutFunctions.playerSprites(player, p, sprites, v, v[SCREENX]) #hitbox

    for i in range(lives+1): #drawing the amount of lives
        screen.blit(livesPic, (10 + 50*i, 80)) #blit the lives in the correct position
    screen.blit(healthPic[2], (0, 0)) #draw the health (in lv3, its always 2)

    display.set_caption("Super Swordy Boy - Level Three     FPS = " + str(int(myClock.get_fps()))) #set the display name
    myClock.tick(60) #60 fps
    display.update() #update the display

def move(p, player, sprites, v):
    'moves the player'
    keys = key.get_pressed()

    leftEnd = 290 #left end of the screen
    rightEnd = 3500 #right end of the screen

    if keys[K_SPACE] and p[Y] + p[H] == v[BOT] and v[Y] == 0: #checking if the player can jump
        jumpSound.play() #play the jump sound
        v[Y] = jumpSpeed #set y-vel to jump speed

    if keys[K_x]: #checking if attacking
        sword.play() #play sword sound
        player[ROW] = 0 #set sprite row to 0

    elif keys[K_LEFT] and p[X] > leftEnd: #checking if trying to move left
        shortcutFunctions.moveGuyLeft(p, player, v, leftEnd, rightEnd) #move left (shortcut functions)

    elif keys[K_RIGHT] and p[X] + p[W] < rightEnd: #checking if trying to move righ
        shortcutFunctions.moveGuyRight(p, player, v, leftEnd, rightEnd) #move right (shortcut functions)

    else: #anything else would result in no movement and idle sprite
        player[COL] = 0
        player[COL] -= 0.2
        v[X] = 0

    player[COL] += 0.2 #add to sprite frame

    if player[COL] >= len(sprites[ROW]): #checking if end of the sprite row
        player[COL] = 1 #set the frame to 1

    p[X] += v[X] #adding horizontal vel to player
    player[X] = p[X]
    v[Y] += gravity #add gravity to vel

    return v #return the velocity to use as parameters in other functions

def check(p, player, sprites, v):
    'checking function'

    hitBox = shortcutFunctions.playerSprites(player, p, sprites, v, v[SCREENX]) #create hitbox

    p[Y] += v[Y] #add vert vel to player
    player[Y] += v[Y] #same thing

    p[H] = hitBox[H] #set players height in rect object to hitbox height
    p[W] = hitBox[W] #same but with width
    

    if p[Y] + hitBox[H] >= GROUND: #checking if the player is trying to go below the ground
        v[BOT] = GROUND #set bottom to ground
        p[Y] = GROUND - hitBox[H] #set player to ground
        v[Y] = 0 #no vert vel

def checkBoss(door, p):
    'check if the door was entered at the end of level 3'
    keys = key.get_pressed()
    if keys[K_RETURN] and p.colliderect(door): #checking if hit enter and collided with the door
        bossDoor.play() #play door sound
        return True #return true for main.py to know to change to boss scene
    return False #if not, return false (here because return acts as a break)


