'''
Joey Zaka and Abbas Zaidi
levelOne.py
Running this will do nothing
Everything that goes on here is to run level one
'''

from pygame import *
from math import *
from shortcutFunctions import *

init()
size = width, height = 1024, 768
myClock = time.Clock()
screen = display.set_mode(size)

backPic = image.load("Backgrounds/background_levelOne.png").convert() #background

GROUND = 677; bottom = GROUND #ground and jump variables for jumping, platforms, etc.
jumpSpeed = -20; gravity = 1

X = 0; Y = 1; W = 2; H = 3; BOT = 2; SCREENX = 3; ROW = 2; COL = 3; TOP = 4 #variables for navigating around lists

v = [0, 0, bottom, 512, 0] #velocity of player

v_bull = [-5, 0] #vel of bullets

v_bird = [0, 0]; vBird_vertical = 10; vBrid_gravity = -1 #velocity of birds

plats = [Rect(900, 525, 200, 15), Rect(3000, 460, 200, 15), Rect(5000, 530, 200, 15), Rect(5400, 450, 200, 15), Rect(6300, 525, 200, 15),
        Rect(6600, 400, 200, 15), Rect(6900, 275, 200, 15)] #platform rect list

blocks = [Rect(1150, 360, 250, 40), Rect(7200, 175, 250, 40)] #blocks rect list

squared_blocks = [Rect(1250, 182, 50, 50), Rect(5475, 250, 50, 50)] #squared blocks rect list

healthSq = [squared_blocks[1]] #health square blocks

slugs = [Rect(2050, 645, 30, 30), Rect(3600, 602, 30, 30), Rect(5700, 645, 30, 30)] #slugs rect list

birds = [Rect(3300, 50, 50, 15), Rect(5300, 50, 50, 15), Rect(1800, 50, 50, 15), Rect(6500, 50, 50, 15), Rect(7500, 50, 50, 15)] #rect list for birds
bird_p = [[birds[i][X], birds[i][Y], 0] for i in range(len(birds))] #make a list instead, based off rect coordinates. this is better for sprites

borders = [Rect(2732, 632, 1366, 47)] #ground border

doorRect = Rect(7305, 100, 40, 75) #rect for door

rapid = 100; sword = 20 #for speed of bullets and sword

isJump = False #variable for checking jumps

health = 2 #beginning health

#time lists and variables
timePassed = []
myCounter = 0

livesPic = image.load('Other/live.png') #lives pic

#sounds
jumpSound = mixer.Sound('audio/effects/Jump.wav')
healthAddition = mixer.Sound('audio/effects/Powerup.wav')
playerDamage = mixer.Sound('audio/effects/Explosion.wav')
movement = mixer.Sound('audio/effects/movement.wav')
movement.set_volume(.05) #lower molume of movement
enterDoor = mixer.Sound('audio/effects/door.wav')
sword = mixer.Sound('audio/effects/sword.wav')

#some text
freshman = font.Font('fonts/Freshman.ttf', 70)
enterText = freshman.render('Press Enter on the Door', True, (2, 26, 112))

def drawScene(screen, p, sprites, player, plats, blocks, sqblocks, slugs, b_slugs, birds, b_s, sprites_b, borders, door, hearts, health, tFont, lives, timePassed, myCounter, v):
    'this function draws the scene'

    if check_levelTwo(door, p):
        screen.fill((0))

    else:
        offset = v[SCREENX]-p[X] #offset to move screen with eveything
        screen.blit(backPic, (offset, 0)) #background
        screen.blit(enterText, (6900 + offset, 400))

        drawPlats(plats, offset) #draws the platforms (shortcut functions)
        moveBlocks(blocks, offset) #moves the blocks with offset shortctu functions
        moveSqBlocks(sqblocks, offset) #moves the squared blocks shortcut functions

        for b in b_s: #birds
            birdHitbox = birdSprites(b, sprites_b, offset) #gets the bird sprites

        for border in borders: #draw borders
            border = border.move(offset, 0) #move border

        #health
        if health > -1: #checking if the player is not dead
            screen.blit(hearts[health], (0, 0)) #blit the hearts

        door = door.move(offset, 0) #door

        pHitbox = playerSprites(player, p, sprites, v, v[SCREENX]) #sprites

        for i in range(lives+1): #to blit the lives on the screen
            screen.blit(livesPic, (10 + 50*i, 80)) #display each picture as a live

        timeFont(tFont, timePassed, 125) #timer in the corner
        if myCounter % 60 == 0: #checking if 1 second has passed
            timePassed.append('t') #add to the time passed list
        myCounter += 1 #counter for the second

        display.update()
        myClock.tick(60)
        display.set_caption("Super Swordy Boy - Level One     FPS = " + str(int(myClock.get_fps()))) #change the name of the window, with fps
        return timePassed, myCounter #to reduce globals

def move(p, player, sprites, blocks, birds, borders, v):
    'this function moves the player'
    keys = key.get_pressed() 


    if keys[K_SPACE] and p[Y] + p[H] == v[BOT] and v[Y] == 0: #checking if it is ok to jump
        v[Y] = jumpSpeed #sets the verticla velocity of the player to the jump speed
        jumpSound.play() #play jump sound

    if keys[K_x]: #checking if the attacking key is clicked
        player[ROW] = 0 #sets the sprite category to attack
        sword.play() #play sword sound


    elif keys[K_LEFT] and p[X] > 400 and hitBlocks(p[X]-5, p[Y], blocks) and hitBlocks(p[X]-5, p[Y], squared_blocks) and hitBlocks(p[X] - 5, p[Y], borders) == -1: #checking if left arrow is clicked and it is ok to move left
        moveGuyLeft(p, player, v, 400, 7550) #move guy functions


    elif keys[K_RIGHT] and p[X] < 12280 and hitBlocks(p[X]+5, p[Y], blocks) and hitBlocks(p[X]+5, p[Y], squared_blocks) and hitBlocks(p[X] + 5, p[Y], borders) == -1: #checking if right arrow is clicked and it is okay to move
        moveGuyRight(p, player, v, 400, 7550) #movement function in shortcut functions

    else: #so the player doesn't move on its own
        player[COL] = 0 #idle position
        player[COL] -= 0.2 #so the frame doesnt move (added later)
        v[X] = 0 #player isnt moving

    player[COL] += 0.2 #increase the frame of 0.2 (increase to speed of frame switching)

    if player[COL] >= len(sprites[ROW]): #checking if the frame number is greater than the amount of sprites in the category
        player[COL] = 1 #sets to the 2nd frame

    p[X] += v[X] #adding the velocity to the players x position
    v[Y] += gravity #add gravity to the player's vertical velocity
    return v #return v to reduce global variables (need v as a parameter because of different modules)

def move_bird(p, birds, bird_p, sprites):
    'this function moves the bird close to the player'
    for b in bird_p: #go through the bird list
         
        if p[X] + 500 >= b[X]: #check if the player is close to the bird horizontally

            v_bird[Y] = vBird_vertical #sets the bird velocity to vertical speed
            v_bird[X] = -8  #sets the bird vel to horizontal one

            if b[X] <= p[X] + 200 and b[Y] >= p[Y]: #checking if same level with player
                v_bird[Y] = 0 #no more vertical movement


            b[ROW] += 0.2 #sprite frame
            
            b[Y] += v_bird[Y] #increase bird pos by vel
            b[X] += v_bird[X] #increasing bird x pos by vel

def check(p, player, sprites, v, plats, slugs, borders, birds, door, healthSq, timePassed, isJump):
    'this function mainly checks for collision'
    global health

    pHitbox = playerSprites(player, p, sprites, v, v[SCREENX]) #sprites

    keys = key.get_pressed()

    if v[Y] != v[BOT]: #checking if in the air
        isJump = True #sets bool variable to true

    for block in blocks: #go through blocks and squared blocks
        for sq in squared_blocks:
            if p[Y] + p[H] >= GROUND or p[Y] + p[H] == v[BOT] or Rect(p[X], p[Y] + 5, p[W], p[H]).colliderect(block) or Rect(p[X], p[Y] + 5, p[W], p[H]).colliderect(sq):
                isJump = False #checked if on top of and set bool variable to false

    for plat in plats: #gp through plats
        if p[X] + p[W] > plat[X] and p[X] < plat[X] + plat[W] and p[Y] + p[H] <= plat[Y] and p[Y] + p[H] + v[Y] > plat[Y]: #check if on top of plat
            v[BOT] = plat[Y] #set bottom to plat y-coord
            p[Y] = v[BOT] - p[H] #set players vert pos to on the platy
            v[Y] = 0 #sets the vertical velocity to 0

    for border in borders: #go through the borders list
        if p[X]+5 + p[W] > border[X] and p[X] < border[X] + border[W] and v[BOT] == GROUND: 
            v[X] = 0

        if p[X] + p[W] > border[X] and p[X] < border[X] + border[W] and p[Y] + p[H] >= border[Y] and p[Y] + p[H] + v[Y] > border[Y]: #checking if on top of
            v[BOT] = border[Y] #same stuff as checking plats below here
            p[Y] = v[BOT] - p[H]
            v[Y] = 0

    for block in blocks: #go through list of blocks
        if isJump and Rect(p[X], p[Y]-5, p[W], p[H]).colliderect(block): #checking if in the air and touching the block from below
            v[TOP] = block[Y] + block[H] #set v top to block
            p[Y] = v[TOP] #set players pos to bottom of block
            v[Y] += gravity #add gravity

        if  not isJump and Rect(p[X], p[Y] + 5, p[W], p[H]).colliderect(block): #checking if not in the air and on a block
            # isJump = False
            v[BOT] = block[Y] #same part as plat here
            p[Y] = v[BOT] - p[H]

            if keys[K_SPACE]: #these next 2 sections are for fixing issues with not being able to jump on blocks
                v[Y] = jumpSpeed #jump

            else:
                v[Y] = 0 #not moving

    for sq in squared_blocks: #go through squared blocks
        if isJump and Rect(p[X], p[Y]-5, p[W], p[H]).colliderect(sq): #same as blocks from before
            v[TOP] = sq[Y] + sq[H] #set v top to bottom of blocks
            #fixes player going above block
            if p[Y] > sq[H] + sq[Y]:
                v[Y] = 0

            else:
                p[Y] = v[TOP]

            v[Y] += gravity #add gravity

        if not isJump and Rect(p[X], p[Y] + 5, p[W], p[H]).colliderect(sq): #same as blocks from before (literally copy and paste wtih adjustments)
            v[BOT] = sq[Y]
            p[Y] = v[BOT] - p[H]

            if keys[K_SPACE]: #these next 2 sections are for fixing issues with not being able to jump on blocks
                v[Y] = jumpSpeed

            else:
                v[Y] = 0

    healthIncrease = 0  #for increasing health

    for h in healthSq: #go through health increase squares
        if isJump and Rect(p[X], p[Y]-5, p[W], p[H]).colliderect(sq) and health < 2: #checking if below the box and touch
            healthAddition.play()
            health = 2

            v[TOP] = sq[Y] + sq[H] #same stuff as blocks here
            #fixes player going above block
            if p[Y] > sq[H] + sq[Y]:
                v[Y] = 0

            else:
                p[Y] = v[TOP]

            v[Y] += gravity
            
    birdCollision(p, player, birds) #bird collision
    check_attack(p, player, sprites, slugs, birds) #checking attacking

    p[Y] += v[Y] #add vert velocity to player 

    if p[Y] + p[H] >= GROUND: #checking if player is on or past ground, dont want the player falling past the ground
        v[BOT] = GROUND #set the bottom to the ground
        p[Y] = GROUND-p[H] #the players y pos to the ground perfectly
        v[Y] = 0 #vertical velocity is 0
    return isJump

def check_attack(p, player, sprites, slugs, birds):
    'checking if the player attacked'
    global health 

    #gets sprites for hitbox
    row = player[ROW]
    col = int(player[COL])

    if row == 0 and col == 5:
        col = 0

    pic = sprites[row][col]
    pHitbox = createHitbox(pic, p[X], p[Y])

    if player[ROW] == 0: #checking if sprites are in attacking position
        for bird in birds: #go through the birds
            birdRect = Rect(bird[X], bird[Y], 100, 80) #create rect object for bird
            if pHitbox.colliderect(birdRect): #check if touched bird
                birds.remove(bird) #removes the bird

def check_levelTwo(door, p):
    'checks if level two door was pressed, this function is used in main.py'
    keys = key.get_pressed()

    if keys[K_RETURN] and p.colliderect(door): #checking if entered the door
        enterDoor.play()
        return True  #returns boolean variable

    else:
        return False #not in the door

def birdCollision(p, player, birds):
    'check bird collision'
    global health 
    
    for bird in birds: #go through the birds
        birdRect = Rect(bird[X], bird[Y], 100, 80) #create rect object for bird
        if birdRect.colliderect(p): #checking if bird touched the player
            birds.remove(bird) #remove the bird
            if player[ROW] == 0: #checking if the player was attacking
                health = health #health remains the same

            else: #if player was not attacking
                playerDamage.play()
                health -= 1 #lower health by 1
                time.delay(150) #this will pause the program for 150ms to indicate you got hit

def hitBlocks(x, y, blocks):
    'check if hit blocks in a list'
    playerRect = Rect(x, y, 35, 50) #creates rect object for the player
    return playerRect.collidelist(blocks) #return if the player collided or not (used in move func)