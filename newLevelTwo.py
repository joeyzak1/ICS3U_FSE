#newLevelTwo.py

from pygame import *
import shortcutFunctions

screen = display.set_mode((1024, 768))
myClock = time.Clock()

#backgrounds and some objects
backPic = image.load('Backgrounds/LevelTwo_backPic.png').convert()
platPic = image.load('Other/plat.png').convert()
doorPic = image.load('Other/doorLev2.png')

#bottom for velocity
GROUND = 574
bottom = GROUND

#jumping variable
jumpSpeed = -20
gravity = 1

#nav variables
X = 0
Y = 1
W = 2
H = 3
ROW = 2
COL = 3
SCREENX = 3
BOT = 2
TOP = 4

#ends of the screen
leftEnd = 50
rightEnd = 15850

health = 2 #health of the player

vPlayer = [0, 0, bottom, 250, 0] #velocity, bottom, etc.

player = [250, 529, 4, 0] #player rect and list
pRect = Rect(250, 529, 4, 0)

plats = [Rect(700, 425, 200, 15), Rect(1550, 425, 200, 15), Rect(8000, 200, 200, 15), Rect(8550, 200, 200, 15), 
        Rect(9000, 287-15, 200, 15), Rect(10050, 425, 200, 15), Rect(11650, 330, 200, 15)] #platforms

#this list branches off into 2d lists - for spikes
spikes = [[Rect(800, 524, 400, 50), Rect(3900, 425, 200, 50), Rect(10000, 524, 400, 50), Rect(13000, 140, 100, 19), Rect(14500, 140, 100, 19), Rect(15000, 140, 100, 19)], #this list is for spikes on the ground or vBOT
        [Rect(3400, 275, 400, 50), Rect(5400, 174, 200, 50), Rect(6000, 174, 200, 50), Rect(11600, 60, 400, 30), Rect(14000, 60, 200, 30)], #this list is for spikes NOT on vBot
        [Rect(1900, 274, 75, 300), Rect(8350, 99, 75, 475)],  #this list is for WALL spikes on vBOT
        [Rect(9400, 0, 75, 374)]] #this list is for WALL spikes NOT on v[BOT]

birds = [[2800, 50, 0], [12000, 50, 0]] #birds list

#seperating borders into 2d lists
borders = [[Rect(2800, 475, 2375, 99), Rect(5175, 374, 100, 200), Rect(5275, 374, 2875, 200), Rect(11500, 475, 500, 99), Rect(12000, 159, 4000, 415)], #borders for touching vBOT
            [Rect(2800, 0, 2100, 275), Rect(4900, 0, 2500, 174), Rect(11500, 0, 100, 275), Rect(11600, 0, 4000, 60)]] #borders for touching top

healthBlocks = [Rect(10125, 200, 50, 50)] #health blocks

doorRect = Rect(15650, 80, 40, 75) #door

#for time
timePassed = []
timeHit = []
myCounter = 0
hitCounter = 0

livesPic = image.load('Other/live.png') #lives picture (the face)

#sounds
jumpSound = mixer.Sound('audio/effects/Jump.wav')
healthAddition = mixer.Sound('audio/effects/Powerup.wav')
playerDamage = mixer.Sound('audio/effects/Explosion.wav')
movement = mixer.Sound('audio/effects/movement.wav')
movement.set_volume(.05)
enterDoor = mixer.Sound('audio/effects/door.wav')
sword = mixer.Sound('audio/effects/sword.wav')

def drawScene(p, player, sprites, plats, platPic, spikes, borders, birds, birdSprites, healthBlocks, healthPicList, door, timeFont, lives, vPlayer, health, timePassed, myCounter, timeHit, hitCounter):
    'draws the scene'

    offset = vPlayer[SCREENX] - p[X] #offset and background
    screen.blit(backPic, (offset, 0))

    shortcutFunctions.drawPlats(plats, offset) #objects to draw
    shortcutFunctions.moveSpikes(spikes, offset)
    shortcutFunctions.drawBorders(borders, offset)
    shortcutFunctions.drawHealthBlocks(healthBlocks, offset)

    door = door.move(offset, 0) #door
    screen.blit(doorPic, door) #door

    if health >= 0: #blit the health only if health remains
        screen.blit(shortcutFunctions.healthBar(health, healthPicList), (0, 0))
    shortcutFunctions.timeFont(timeFont, timePassed, 300) #blits the time in the corner

    for b in birds: #go through the birds
        shortcutFunctions.birdSprites(b, birdSprites, offset) 
    
    hitBox = shortcutFunctions.playerSprites(player, p, sprites, vPlayer, vPlayer[SCREENX]) #hit counter

    if myCounter % 60 == 0: #for time
        timePassed.append('t')
    for spike in spikes: #to try with spikes (possibly remove later)
        if p.collidelist(spike) != -1:
            timeHit.append('h')

        else:
            for t in timeHit:
                timeHit.remove(t)

    for i in range(lives+1):
        screen.blit(livesPic, (10 + 50*i, 80))

    #same things as level one
    myCounter += 1
    hitCounter += 1
    display.set_caption("Super Swordy Boy - Level Two     FPS = " + str(int(myClock.get_fps())))
    display.update()
    myClock.tick(60)
    return timePassed, myCounter, timeHit #to reduce globals

def move(p, player, sprites, borders, spikes, vPlayer):
    'this function moves the guy'
    keys = key.get_pressed()

    #left and right end of the screen
    leftEnd = 230
    rightEnd = 15850

    hitBox = shortcutFunctions.playerSprites(player, p, sprites, vPlayer, vPlayer[SCREENX]) #hitbox

    if keys[K_SPACE] and p[Y] + hitBox[H] == vPlayer[BOT] and vPlayer[Y] == 0 and shortcutFunctions.hitSpikes(p[X], p[Y] - 5, hitBox, spikes) == -1: #checking if it is ok to jump
        jumpSound.play() #play the jump sound
        vPlayer[Y] = jumpSpeed #go to jump speed

    if keys[K_x]: #checking if its ok to attack
        sword.play() #play sword sound
        player[ROW] = 0 #set sprite frame category to 0

    # for border in borders:
    elif keys[K_LEFT] and shortcutFunctions.hitSpikes(p[X] - 5, p[Y], hitBox, spikes) == -1 and shortcutFunctions.hitSpikes(p[X] - 5, p[Y], hitBox, borders) == -1 and p[X] > leftEnd: #checking if it is ok to go left
        shortcutFunctions.moveGuyLeft(p, player, vPlayer, leftEnd, rightEnd) #move left

    elif keys[K_RIGHT] and shortcutFunctions.hitSpikes(p[X] + 5, p[Y], hitBox, spikes) == -1 and shortcutFunctions.hitSpikes(p[X] + 5, p[Y], hitBox, borders) == -1: #checking if it is ok to go right
        shortcutFunctions.moveGuyRight(p, player, vPlayer, leftEnd, rightEnd) #move right

    #rest of the function is the same as level one

    else:
        player[COL] = 0
        player[COL] -= 0.2
        vPlayer[X] = 0

    # print(shortcutFunctions.hitSpikes(p[X] + 5, p[Y], hitBox, spikes), shortcutFunctions.hitSpikes(p[X] - 5, p[Y], hitBox, spikes))


    player[COL] += 0.2

    if player[COL] >= len(sprites[ROW]):
        player[COL] = 1

    p[X] += vPlayer[X]
    player[X] = p[X]
    vPlayer[Y] += gravity

    return vPlayer #to reduce globals


def moveBad(player, bird):
    'moves the bird (had an old plan to move multiple)'
    shortcutFunctions.moveBird(player, birds) #moves the bird


def check(p, player, sprites, plats, spikes, borders, healthBlocks, healthPicList, birds, timePassed, timeHit, vPlayer, health, hitCounter):
    'checks for collision, etc.'

    hitBox = shortcutFunctions.playerSprites(player, p, sprites, vPlayer, vPlayer[SCREENX]) #hitbox of player

    for plat in plats: #go through the platforms
        if p[X] + p[W] > plat[X] and p[X] < plat[X] + plat[W] and p[Y] + p[H] <= plat[Y] and p[Y] + p[H] + vPlayer[Y] > plat[Y]: #normal like other levels
            vPlayer[BOT] = plat[Y]
            p[Y] = vPlayer[BOT] - p[H]
            vPlayer[Y] = 0
            if p[Y] + hitBox[H] >= plat[Y]: #this is so the player doesnt fall through the platform (weird issue)
                p[Y] = plat[Y] - hitBox[H] #do the same as above
                vPlayer[Y] = 0

    for h in healthBlocks: #go through health increase squares
        if vPlayer[Y] < 0 and Rect(p[X], p[Y]-5, p[W], p[H]).colliderect(h) and health <= 2: #checking if below the box and touch
            if health < 2: #will only do if health isnt full
                healthAddition.play() #play health addition noise
                health = 2 #health is now full

            vPlayer[TOP] = h[Y] + h[H] #same stuff as blocks here (see level one for comments here)
            #fixes player going above health sq
            if p[Y] > h[H] + h[Y]: #checking if the player is below
                vPlayer[Y] = 0

            else: #anything else 
                p[Y] = vPlayer[TOP] #v top would be player y pos

            vPlayer[Y] += gravity #add gravity so the player goes off

    # shortcutFunctions.checkSpikes(p, hitBox, spikes, vPlayer, health, timeHit) not needed anymore
    shortcutFunctions.checkBorders(p, hitBox, vPlayer, borders) #checks if player is on borders

    p[Y] += vPlayer[Y] #incerase player y by vel
    # player[Y] += vPlayer[Y]


    p[W] = hitBox[W] #sets p width and height to hitbox w and h
    p[H] = hitBox[H]

    # print(health)

    for spike in spikes: #this loop checks if the player touches the spikes at all
        # if len(timePassed) % 2 == 0:
        if Rect(p[X] + 5, p[Y], hitBox[W], hitBox[H]).collidelist(spike) != -1 \
            or Rect(p[X] - 5, p[Y], hitBox[W], hitBox[H]).collidelist(spike) != -1 \
                or Rect(p[X], p[Y] + 5, hitBox[W], hitBox[H]).collidelist(spike) != -1\
                    or Rect(p[X] - 5, p[Y], hitBox[W], hitBox[H]).collidelist(spike) != -1:
            playerDamage.play() #damage sound
            health = -1 #dies

    for bird in birds: #go through birds
        bRect = Rect(bird[X], bird[Y], 226, 189) #create a rect for the bird (same size as sprite)
        if p.colliderect(bRect) and player[ROW] != 0: #checking if the player touches the bird
            playerDamage.play() #play damage sound
            health -= 1 #decrease health by 1
            birds.remove(bird) #remove bird from screen
        elif p.colliderect(bRect) and player[ROW] == 0:
            birds.remove(bird)

    if p[Y] + hitBox[H] >= GROUND: #same as other levels here, so the player doesnt go below the ground
        vPlayer[BOT] = GROUND 
        p[Y] = GROUND - hitBox[H]
        vPlayer[Y] = 0

    return health, hitCounter #to reduce global variables