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

platGrav = False #not needed anymore

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

plats = [Rect(600, 425, 200, 15), Rect(1550, 425, 200, 15), Rect(8000, 200, 200, 15), Rect(8550, 200, 200, 15), 
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

platCounter = 0 

#for time
timePassed = []
timeHit = []
myCounter = 0
hitCounter = 0

livesPic = image.load('Other/live.png')


def drawScene(p, player, sprites, plats, platPic, spikes, borders, birds, birdSprites, healthBlocks, healthPicList, door, timeFont, lives):
    'draws the scene'
    global vPlayer
    global health
    global timePassed
    global myCounter
    global timeHit
    global hitCounter

    offset = vPlayer[SCREENX] - p[X] #offset and background
    screen.blit(backPic, (offset, 0))

    shortcutFunctions.drawPlats(plats, offset, platPic) #objects to draw
    shortcutFunctions.drawSpikes(spikes, offset)
    shortcutFunctions.drawBorders(borders, offset)
    shortcutFunctions.drawHealthBlocks(healthBlocks, offset)

    door = door.move(offset, 0) #door
    screen.blit(doorPic, door) #door

    if health >= 0: #blit the health only if health remains
        screen.blit(shortcutFunctions.healthBar(health, healthPicList), (0, 0))
    shortcutFunctions.timeFont(timeFont, timePassed, 300) #blits the time in the corner

    for b in birds: #go through the birds
        shortcutFunctions.birdSprites(b, birdSprites, offset) 

    
    shortcutFunctions.playerSprites(player, p, sprites, vPlayer, vPlayer[SCREENX]) #sprites
    hitBox = shortcutFunctions.playerSprites(player, p, sprites, vPlayer, vPlayer[SCREENX])
    # draw.rect(screen, (255, 0, 0), [vPlayer[SCREENX], p[Y], hitBox[W], hitBox[H]], 2) #hitbox drawing

    if myCounter % 60 == 0: #for time
        timePassed.append('t')
    for spike in spikes:
        if p.collidelist(spike) != -1:
            timeHit.append('h')

        else:
            for t in timeHit:
                timeHit.remove(t)

    for i in range(lives):
        screen.blit(livesPic, (10 + 50*i, 80))

    # print(timePassed)

    
    # print(p[X])
    myCounter += 1
    hitCounter += 1
    display.set_caption("Super Swordy Boy - Level Two     FPS = " + str(int(myClock.get_fps())))
    display.update()
    myClock.tick(60)

def move(p, player, sprites, borders, spikes):
    global vPlayer
    global leftEnd
    global rightEnd
    global health
    global platGrav

    shortcutFunctions.playerSprites(player, p, sprites, vPlayer, vPlayer[SCREENX])
    hitBox = shortcutFunctions.playerSprites(player, p, sprites, vPlayer, vPlayer[SCREENX])

    keys = key.get_pressed()

    if keys[K_SPACE] and p[Y] + hitBox[H] == vPlayer[BOT] and vPlayer[Y] == 0 and shortcutFunctions.hitSpikes(p[X], p[Y] - 5, hitBox, spikes) == -1:
        vPlayer[Y] = jumpSpeed

    if keys[K_LEFT] and shortcutFunctions.hitSpikes(p[X] - 5, p[Y], hitBox, spikes) == -1:
        shortcutFunctions.moveGuyLeft(p, player, vPlayer, leftEnd, rightEnd)

    elif keys[K_RIGHT] and shortcutFunctions.hitSpikes(p[X] + 5, p[Y], hitBox, spikes) == -1:
        shortcutFunctions.moveGuyRight(p, player, vPlayer, leftEnd, rightEnd)


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
    # if platGrav == False:
    # if platCounter != 1:
    vPlayer[Y] += gravity
    if platCounter == 1:
        vPlayer[Y] = 0


def moveBad(player, bird):
    shortcutFunctions.moveBird(player, birds)


def check(p, player, sprites, plats, spikes, borders, healthBlocks, healthPicList, birds, timePassed, timeHit):
    global health
    global vPlayer
    global platGrav
    global platCounter
    global hitCounter
    # global timeHit

    invincibility = 0


    

    shortcutFunctions.playerSprites(player, p, sprites, vPlayer, vPlayer[SCREENX])
    hitBox = shortcutFunctions.playerSprites(player, p, sprites, vPlayer, vPlayer[SCREENX])

    # shortcutFunctions.checkPlats(plats, p, player,hitBox, vPlayer)
    # platCounter = 0
    # for plat in plats:
    #     if p[X] + p[W] > plat[X] and p[X] < plat[X] + plat[W] and p[Y] + p[H] <= plat[Y] and p[Y] + p[H] + vPlayer[Y] > plat[Y]: #check if player is ON TOP of platform
    #         vPlayer[BOT] = plat[Y] #set v bottom to platform y coord
    #         p[Y] = vPlayer[BOT] - p[H] #set player pos [Y] to plat
    #         vPlayer[Y] = 0 #set player y velocity to 0
    #         platCounter += 1
    for plat in plats:
        if p[X] + p[W] > plat[X] and p[X] < plat[X] + plat[W] and p[Y] + p[H] <= plat[Y] and p[Y] + p[H] + vPlayer[Y] > plat[Y]:
            vPlayer[BOT] = plat[Y]
            p[Y] = vPlayer[BOT] - p[H]
            vPlayer[Y] = 0
            if p[Y] + hitBox[H] >= plat[Y]:
                p[Y] = plat[Y] - hitBox[H]
                vPlayer[Y] = 0

    for h in healthBlocks: #go through health increase squares
        if vPlayer[Y] < 0 and Rect(p[X], p[Y]-5, p[W], p[H]).colliderect(h) and health <= 2: #checking if below the box and touch
            if health < 2:
                health += 1
            # healthIncrease += 1
        #for health increments
        # if healthIncrease == 1:
        #     if health == 0:
        #         health = 1

        #     elif health == 1:
        #         health = 2
            # if health < 2:
            #     health += 1

            # else:
            #     health = health

            vPlayer[TOP] = h[Y] + h[H] #same stuff as blocks here
            #fixes player going above block
            if p[Y] > h[H] + h[Y]:
                vPlayer[Y] = 0

            else:
                p[Y] = vPlayer[TOP]

            vPlayer[Y] += gravity
    

    # print(plats[5], p[X], p[Y], vPlayer)

    shortcutFunctions.checkSpikes(p, hitBox, spikes, vPlayer, health, timeHit)
    shortcutFunctions.checkBorders(p, hitBox, vPlayer, borders)
    shortcutFunctions.checkBirdCollision(birds, p, health)

    # for plat in plats:
    #     if p[X] + hitBox[W] > plat[X] and p[X] < plat[X] + plat[W] and p[Y] + hitBox[H] <= plat[Y] and p[Y] + hitBox[H] + vPlayer[Y] > plat[Y]:
    #         vPlayer[BOT] = plat[Y]
    #         p[Y] = vPlayer[BOT] - hitBox[H]
    #         vPlayer[Y] = 0

    p[Y] += vPlayer[Y]
    # player[Y] += vPlayer[Y]


    p[W] = hitBox[W]
    p[H] = hitBox[H]

    # print(health)

    for spike in spikes:
        # if len(timePassed) % 2 == 0:
        if Rect(p[X] + 5, p[Y], hitBox[W], hitBox[H]).collidelist(spike) != -1 \
            or Rect(p[X] - 5, p[Y], hitBox[W], hitBox[H]).collidelist(spike) != -1 \
                or Rect(p[X], p[Y] + 5, hitBox[W], hitBox[H]).collidelist(spike) != -1\
                    or Rect(p[X] - 5, p[Y], hitBox[W], hitBox[H]).collidelist(spike) != -1:
            health = -1

    for bird in birds:
        bRect = Rect(bird[X], bird[Y], 226, 189)
        if p.colliderect(bRect):
            health -= 1
            birds.remove(bird)

            # if invincibility > 0:
            #     invincibility += 1
    # for h in timeHit:
    #     timeHit.remove(h)


    

    if p[Y] + hitBox[H] >= GROUND:
        vPlayer[BOT] = GROUND
        p[Y] = GROUND - hitBox[H]
        vPlayer[Y] = 0

    # if hitCounter % 60 == 0:
    #     hitList.append('h')
    # hitCounter += 1



    # if p[Y] + hitBox[H] >= vPlayer[BOT]:
    #     p[Y] = vPlayer[BOT] - hitBox[H]
    #     vPlayer[Y] = 0
