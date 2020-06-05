#shortcutFunctions.py
# this program has useful functions that can shorten code
from pygame import *
from math import*

init()

screen = display.set_mode((1024, 768))

jumpSpeed = -20; gravity = 1 #for jumping

X = 0; Y = 1; W = 2; H = 3; BOT = 2; SCREENX = 3; ROW = 2; COL = 3; TOP = 4 #navigation variables

#bird vel's
vel_bird = [0, 0]
vBird_vertical = 10
vBrid_gravity = -1

playerHealth = 2 #player health (not used)

#other pics
platPic = image.load('Other/plat.png').convert()
healthBlock = image.load('Other/healthBox.png').convert()

#sound effects
jumpSound = mixer.Sound('audio/effects/Jump.wav')
healthAddition = mixer.Sound('audio/effects/Powerup.wav')
playerDamage = mixer.Sound('audio/effects/Explosion.wav')
movement = mixer.Sound('audio/effects/movement.wav')
movement.set_volume(.05) #lower the volume
enterDoor = mixer.Sound('audio/effects/door.wav')
sword = mixer.Sound('audio/effects/sword.wav')
timeTicking = mixer.Sound('audio/effects/timeTickingLong.wav')

def drawPlats(plats, offset):
    'this function draws platforms with offset. the platforms must be in a LIST, and must be Rect objects, pic is a pic of a plat'
    # global offset
    for plat in plats: #taking every element from list of plats
        plat = plat.move(offset, 0)
        screen.blit(platPic, (plat[X], plat[Y])) #blitting each plat pic in plat pos

def moveSpikes(spikes, offset):
    'this functions draws spikes'
    for sp in spikes: 
        for ground in sp: #went through two loops to get to desired spikes (2d list)
            ground = ground.move(offset, 0) #move according to offset

def moveBlocks(blocks, offset):
    'this function draws blocks - blocks must be in a LIST and have offset'
    for block in blocks: #go through all the blocks
        block = block.move(offset, 0) #move the blocks

def moveSqBlocks(sq_blocks, offset):
    'this function draws squared blocks - param needs to be a list'
    for sq in sq_blocks: #go through squared blocks
        sq = sq.move(offset, 0) #moves it according to offset

def drawHealthBlocks(healthB, offset):
    'this function draws the health blocks'
    for h in healthB: #go through health blocks
        h = h.move(offset, 0) #move the block
        screen.blit(healthBlock, h) #blit health pic

def drawBorders (borders, offset):
    'this function draws borders'
    for lists in borders: #go through all lists in borders
        for border in lists: #go through each rect in the lists
            border = border.move(offset, 0) #move the borders according to offset
 
def createHitbox (pic, x, y):
    'this function creates a hitbox'
    pic_width = pic.get_width() #get the width of the sprite frame
    pic_height = pic.get_height() #get the height of the sprite frame
    hitbox = Rect (x, y, pic_width, pic_height) #create rect object with width and height
    return hitbox #return the hitbox rect

def playerSprites (player, p, sprites, vPlayer, x):
    'this function gets the sprite of a character'
    row = player[ROW] #get the row of the player, its player[2]
    col = int(player[COL]) #get the col of the sprites, its player[4], this is the frame
    if row == 0 and col == 5: #checking if on attacking (to prevent crash)
        col = 0 #set the sprite to first frame 
    pic = sprites[row][col] #get the pic from the sprites list
    pictureRect = createHitbox(pic, x, p[Y]) #call hitbox function to get the pic rect
    screen.blit(pic, pictureRect) #blits the picture
    return pictureRect #returns the pic rect

def createBossBullets(bullets, SPEED, bossR, rapid):
    'create boss bullets'
    for i in range(12):
        ang = atan2(bossR[Y], bossR[X]) #gets the angle
        ang *= i #multiply the angle by i (for multiple angles)
        vx = cos(ang)*SPEED #horizontal component
        vy = sin(ang)*SPEED #vertical component
        if len(bullets) < 12:
            bullets.append([bossR[X], bossR[Y], vx, vy]) #add to bullet list
    
def moveGuyLeft(p, player, vPlayer, leftEnd, rightEnd):
    'this function moves the guy to the left'
    keys = key.get_pressed()
    if p[X] + 5 < rightEnd: #checking if the player is not at the end point
        movement.play() #play movement sound
        player[ROW] = 3 #moving left sprite
        if keys[K_LSHIFT] or keys[K_RSHIFT]: #checking if the shift key(s) were clicked 
            vPlayer[X] = -10 #doubles the speed of the player
        else: #if no shift
            vPlayer[X] = -5 #normal speed
        if vPlayer[SCREENX] > 350: #so the player stays on the screen while running
            vPlayer[SCREENX] -= 5 #move the screen itself
    elif p[X] > rightEnd: #checking if past the right end
        movement.play() #movement sound
        if keys[K_LSHIFT] or keys[K_RSHIFT]: #checking if the shift key(s) were clicked 
            vPlayer[X] = -10 #doubles the speed of the player
        else: #if no shift
            vPlayer[X] = -5 #normal speed

def moveGuyRight(p, player, vPlayer, leftEnd, rightEnd):
    'this function moves the guy to the right'
    keys = key.get_pressed()
    if p[X] + 5 < rightEnd: #checking if the player is touching the right end
        player[ROW] = 4 #sprite category to 4 (running right)
        movement.play() #movement sound
        if keys[K_LSHIFT] or keys[K_RSHIFT]: #checking if the shift key(s) were clicked 
            vPlayer[X] = 10 #doubles the speed of the player
        else: #if no shift
            vPlayer[X] = 5 #normal speed
        if vPlayer[SCREENX] < 700: #so the player stays on the screen while running
            vPlayer[SCREENX] += 5 #move the screen itself
    elif p[X] > rightEnd: #checking if the player is beyond the end
        player[ROW] = 4 #putting the sprite in idle
        player[COL] = 0
        if vPlayer[X] > 0: #checking if the player is trying to move right
            vPlayer[X] = 0 #won't allow it

def moveGuyLeftBoss(p, player, vPlayer, leftEnd, rightEnd):
    'this function moves the guy to the left only for boss'
    keys = key.get_pressed()
    if p[X] + 5 < rightEnd: #checking if the player is not at the end point
        movement.play() #play movement sound
        player[ROW] = 3 #moving left sprite
        if keys[K_LSHIFT] or keys[K_RSHIFT]: #checking if the shift key(s) were clicked 
            vPlayer[X] = -10 #doubles the speed of the player
        else: #if no shift
            vPlayer[X] = -5 #normal speed
    elif p[X] > rightEnd: #checking if past the right end
        movement.play() #movement sound
        if keys[K_LSHIFT] or keys[K_RSHIFT]: #checking if the shift key(s) were clicked 
            vPlayer[X] = -10 #doubles the speed of the player
        else: #if no shift
            vPlayer[X] = -5 #normal speed

def moveGuyRightBoss(p, player, vPlayer, leftEnd, rightEnd):
    'this function moves the guy to the right, see moveGuyRight() for comments'
    keys = key.get_pressed()
    if p[X] + 5 < rightEnd:
        player[ROW] = 4
        movement.play()
        if keys[K_LSHIFT] or keys[K_RSHIFT]: #checking if the shift key(s) were clicked 
            vPlayer[X] = 10 #doubles the speed of the player
        else: #if no shift
            vPlayer[X] = 5 #normal speed
    elif p[X] > rightEnd:
        player[ROW] = 4
        player[COL] = 0
        if vPlayer[X] > 0:
            vPlayer[X] = 0

def moveBird(player, birds):
    'moving the bird when close to the player'
    for bird in birds: #going through the birds list
        if player[X] + 500 >= bird[X]: #checking if the player + 400 px is >= birds x val
            vel_bird[Y] = vBird_vertical #sets the birds y velocty
            vel_bird[X] = -8 #set the bird x velocity
            if bird[X] <= player[X] + 200 and bird[Y] >= player[Y]: # checking if bird [y] val is close to player y val
                vel_bird[Y] = 0 #stop moving VERTICALLY
            bird[ROW] += 0.2 #frame for sprite
            bird[Y] += vel_bird[Y] #move the bird
            bird[X] += vel_bird[X]

def birdSprites(bird, sprites, offset):
    'get the bird sprites'
    # for b in birds:
    row = int(bird[ROW]) #get the frame
    if row > 4: #for crashes
        row = 0
    pic = sprites[row] #get the pic (1-d array)
    pictureRect = createHitbox(pic, bird[X], bird[Y]) #create a hitbox w previous function
    pictureRect = pictureRect.move(offset, 0) #same as previous sprite function
    screen.blit(pic, pictureRect) #blit bird pic
    return pictureRect

def checkBorders(p, hitbox, vPlayer, borders):
    'checking if borders are touched'
    for b in borders[0]: #go through borders on ground
        if p[X] + hitbox[W] > b[X] and p[X] < b[X] + b[W] and p[Y] + hitbox[H] >= b[Y] and p[Y] + hitbox[H] + vPlayer[Y] > b[Y]: #check if player is on top
            vPlayer[BOT] = b[Y] #sets bottom to border
            p[Y] = vPlayer[BOT] - hitbox[H] #sets player pos on the border
            vPlayer[Y] = 0 #no vert vel

    for b in borders[1]: #go through borders touching the top of the screen
        if Rect(p[X], p[Y], hitbox[W], hitbox[H]).colliderect(b): #check if the player touches it
            vPlayer[TOP] = b[Y] + b[H] #top is the end of the vertical border
            p[Y] = vPlayer[TOP] #the player's y pos is the end of the border
            if p[Y] > b[H] + b[Y]: #checking if the player is gping into the border
                vPlayer[Y] = 0 #player stops moving vertically
                vPlayer[Y] += 1

def checkDoor(p, door):
    'checks if a door is enetered'
    keys = key.get_pressed()
    if keys[K_RETURN] and p.colliderect(door): #checks if the player enters a door by hitting enter
        return True
    return False

def timeFont(font, timePassed, length):
    '''this function creates a timer for the level, which counts DOWN 
    - font is the font requred for the time
    - timePassed is the list for counting the time
    - Length is the length of how long the level will give you'''
    text = font.render(str(int(length-len(timePassed))), True, (255, 255, 255)) #get the text by taking the length of the level minus length of list, convert to string
    if length - len(timePassed) < 6:
        text = font.render(str(int(length-len(timePassed))), True, (255, 0, 0)) #get the text by taking the length of the level minus length of list, convert to string
        timeTicking.play()
    text2 = font.render(str(int(length-len(timePassed))), True, (0, 0, 0)) #get the text by taking the length of the level minus length of list, convert to string
    screen.blit(text2, (942, 5)) #shadow
    screen.blit(text, (940, 3)) #blit the text