#shortcutFunctions.py
# this program has useful functions that can shorten code
from pygame import *
from math import *

screen = display.set_mode((1024, 768))

jumpSpeed = -20; gravity = 1

X = 0; Y = 1; W = 2; H = 3; BOT = 2; SCREENX = 3; ROW = 2; COL = 3; TOP = 4

vel_bird = [0, 0]
vBird_vertical = 30
vBrid_gravity = -1

def drawPlats(plats, offset, pic):
    'this function draws platforms with offset. the platforms must be in a LIST, and must be Rect objects, pic is a pic of a plat'
    # global offset
    for plat in plats: #taking every element from list of plats
        plat = plat.move(offset, 0)
        screen.blit(pic, (plat[X], plat[Y])) #blitting each plat pic in plat pos

def drawSpikes(spikes, offset):
    'this functions draws spikes'
    for sp in spikes: 
        for ground in sp: #went through two loops to get to desired spikes (2d list)
            ground = ground.move(offset, 0) #move according to offset

def drawBlocks(blocks):
    'this function draws blocks - blocks must be in a LIST and have offset'
    for block in blocks: #this loop blits all blocks
        block = block.move(offset, 0)
        draw.rect(screen, (255, 0, 0), block) #draws the block

def drawSqBlocks(sq_blocks):
    'this function draws squared blocks - param needs to be a list'
    for sq in sq_blocks: #this for loop blits all squared blocks
        sq = sq.move(offset, 0)
        draw.rect(screen, (0, 0, 255), sq)

def drawHealthBlocks(healthB, offset):
    'this function draws the health blocks'
    for h in healthB:
        h = h.move(offset, 0)
        draw.rect(screen, (0, 0, 255), h)

def drawSlugs(slugs):
    'this function draws slugs - work on these LATER'
    return 1 

def drawBorders (borders, offset):
    'this function draws borders'
    for lists in borders: #go through all lists in borders
        for border in lists:
            border = border.move(offset, 0)

def drawTempBird(birds, offset):
    'old func'
    for bird in birds:
        bird = bird.move(offset, 0)
        draw.rect(screen, (120, 255, 89), [bird[X], bird[Y], 60, 30])

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

# boss bullets --------------------------------------------------
def drawBossBullets(bullets):
    'draws boss bullets'
    for b in bullets: #go through the bullets list
        draw.circle(screen, (0, 255, 0), (int(b[0]),int(b[1])), 4) #draw the bullet

def createBossBullets(bullets, SPEED, bossR, rapid):
    'create boss bullets'
    if rapid < 20:#for how often bullets appear
        rapid += 1 #increase by 1

    if rapid == 20: #checking if time is right
        for i in range(12):
            ang = atan2(bossR[Y] - 318, bossR[X] - 424) #gets the angle
            ang *= i #multiply the angle by i (for multiple angles)
            vx = cos(ang)*SPEED #horizontal component
            vy = sin(ang)*SPEED #vertical component
            bullets.append([bossR[X], bossR[Y], vx, vy]) #add to bullet list
        rapid = 0 #set rapid to 0
    

def checkBossBullets(bullets):
    'check and move boss bullets'
    for b in bullets[:]: #[:] is a COPY of the bullets list, goes through bullets list
        b[0] += b[2] #add x val to speed
        b[1] += b[3] #add y-val to speed

        if b[0] > 978 or b[0] < 46 or b[1] < 0 or b[1] > 722: #off screen
            bullets.remove(b) #remove from screen

def createBossBulletsPhase2(bullets, rapid, boss):
    if rapid == 20:
        bullets.append([boss[X], boss[Y], -5, 0])

    if rapid < 20:
        rapid += 1


#move boss between attacks ------------------------------------
def moveBossBetween(boss, b, v, time):
    # if len(time) > 15:
        # v[X] = -3
        # if b[X] > 400:
        #     v[X] = 0
    v[X] = 0
    for i in range(2):
        if b[X] > 300:
            v[X] = -3
                

            # elif  < b[X] < 625:
            #     v[X] = 3

#move boss close to player
def moveBossPhaseTwo(boss, b, v, player):
    gravityBoss = 3
    bossUp = -15
    if b[Y] < 0:
        b[Y] += bossUp

    # v[Y] += gravityBoss








def checkPlats(plats, p, player, hitBox, v):
    'checking for platform collision'
    # for plat in plats:
    #     if p[X] + hitBox[W] > plat[X] and p[X] < plat[X] + plat[W] and p[Y] + hitBox[H] <= plat[Y] and p[Y] + hitBox[H] + vPlayer[Y] > plat[Y]:
    #         vPlayer[BOT] = plat[Y]
    #         p[Y] = vPlayer[BOT] - hitBox[H]
    #         player[Y] = vPlayer[BOT] - hitBox[H]
    #         vPlayer[Y] = 0
    for plat in plats:
        if p[X] + p[W] > plat[X] and p[X] < plat[X] + plat[W] and p[Y] + p[H] <= plat[Y] and p[Y] + p[H] + v[Y] > plat[Y]: #check if player is ON TOP of platform
            v[BOT] = plat[Y] #set v bottom to platform y coord
            p[Y] = v[BOT] - p[H] #set player pos [Y] to plat
            v[Y] = 0 #set player y velocity to 0





def moveGuyLeft(p, player, vPlayer, leftEnd, rightEnd):
    'this function moves the guy to the left'
    keys = key.get_pressed()

    if leftEnd < p[X] + 5 < rightEnd: #checking if player is offscreen
        player[ROW] = 3 #set sprite row to left moving
        vPlayer[X] = -5 #set velocity of player to -5 (left moving)
        if keys[K_LSHIFT] or keys[K_RSHIFT]: #checking if chift was held
            vPlayer[X] = -10 #increase velocity
        if vPlayer[SCREENX] > 250: #checking if screen pos is correct
            vPlayer[SCREENX] -= 5 

    elif p[X] > rightEnd: #checking if right end is touched
        if vPlayer[X] == 0: #checking if players velocity is 0
            if keys[K_LSHIFT] or keys[K_RSHIFT]: #if shift clicked
                vPlayer[X] = -10 #v = -10 (left faster)
            else: #anything else
                vPlayer[X] = -5 #v = -5 (slower)


def moveGuyRight(p, player, vPlayer, leftEnd, rightEnd):
    'this function moves the guy to the right'
    keys = key.get_pressed()

    if leftEnd < p[X] + 5 < rightEnd: #checking if good with borders
        player[ROW] = 4 #sprite row to right moving 
        vPlayer[X] = 5 #player x velocity set to 5 (moving right)
        if keys[K_LSHIFT] or keys[K_RSHIFT]: #checking if shift is clicked
            vPlayer[X] = 10 #v = 10 (faster)
        if vPlayer[SCREENX] < 700: #checking if good with screen pos
            vPlayer[SCREENX] += 5 #increase by 5

    elif p[X] > rightEnd: #checking if good with right end of level
        player[COL] = 0 #cannot move, therefore must be in idle position
        if vPlayer[X] > 0: #checking if trying to move
            vPlayer[X] = 0 #then he cant move

def moveGuyLeftBoss(p, player, vPlayer, leftEnd, rightEnd):
    'this function moves the guy to the left only for boss'
    keys = key.get_pressed()

    if leftEnd < p[X] + 5 < rightEnd:
        player[ROW] = 3
        vPlayer[X] = -5
        if keys[K_LSHIFT] or keys[K_RSHIFT]:
            vPlayer[X] = -10

    elif p[X] > rightEnd:
        if vPlayer[X] == 0:
            if keys[K_LSHIFT] or keys[K_RSHIFT]:
                vPlayer[X] = -10
            else:
                vPlayer[X] = -5

def moveGuyRightBoss(p, player, vPlayer, leftEnd, rightEnd):
    'this function moves the guy to the right'
    keys = key.get_pressed()

    if leftEnd < p[X] + 5 < rightEnd:
        player[ROW] = 4
        vPlayer[X] = 5
        if keys[K_LSHIFT] or keys[K_RSHIFT]:
            vPlayer[X] = 10

    elif p[X] > rightEnd:
        player[COL] = 0
        if vPlayer[X] > 0:
            vPlayer[X] = 0

#bird ----------------------------------------------------------------------------
def moveBird(player, birds):
    for bird in birds:
        if player[X] + 400 >= bird[X]:
            vel_bird[Y] = vBird_vertical
            vel_bird[X] = -15

            if bird[X] <= player[X] + 200 and bird[Y] >= player[Y]:
                vel_bird[Y] = 0

            bird[ROW] += 0.2

            bird[Y] += vel_bird[Y]
            bird[X] += vel_bird[X]

def birdSprites(bird, sprites, offset):
    # for b in birds:
    row = int(bird[ROW])
    if row > 4:
        row = 0
    pic = sprites[row]
    pictureRect = createHitbox(pic, bird[X], bird[Y])
    pictureRect = pictureRect.move(offset, 0)
    screen.blit(pic, pictureRect)
    return pictureRect

def checkBirdCollision(birds, p, health):
    # if p.collidelist(birds):
    for bird in birds:
        birdRect = Rect(bird[X], bird[Y], 100, 80)
        if p.colliderect(birdRect):
            health -= 1
            if health < 0:
                health = 0


def checkSpikes(p, hitbox, spikes, vPlayer, health):
    # for spike in spikes:
    #     for sp in spike:
    #         if Rect(p[X], p[Y], hitbox[W], hitbox[H]).colliderect(sp):
    #             health -= 1
    #             if health < 0:
    #                 health = 0
            
    for grnd in spikes[0]:
        if p[X] + hitbox[W] > grnd[X] and p[X] < grnd[X] + grnd[W] and p[Y] + hitbox[H] >= grnd[Y] and p[Y] + hitbox[H] + vPlayer[Y] > grnd[Y]:
            vPlayer[BOT] = grnd[Y]
            p[Y] = vPlayer[BOT] - hitbox[H]
            vPlayer[Y] = 0

    for air in spikes[1]:
        if vPlayer[Y] > 0 and p.collidelist(spikes[1]) != -1:
            vPlayer[TOP] = air[Y] + air[H]
            p[Y] = vPlayer[TOP]
            vPlayer[Y] = 0

            

    # for air in spikes[1]:
    #     # if p[X] + 5  + hitbox[W] == air[X]:
    #     #     vPlayer[X] = 0
    #     #     p[X] = air[X] - 5

    #     # elif p[X] - 5 == air[X] + air[W]:
    #     #     vPlayer[X] = 0 
    #     #     p[X] = air[X] + air[W] + 5
    #     #     p[Y] = vPlayer[BOT] - hitbox[H]

    #     if Rect(p[X], p[Y], hitbox[W], hitbox[H]).colliderect(air):
    #         vPlayer[TOP] = air[Y] + air[H]
    #         p[Y] = vPlayer[TOP]
    #         if p[Y] > air[H] + air[Y]:
    #             vPlayer[Y] = 0

    # for wall in spikes[2]:
    #     if p[X] + hitbox[W] > wall[X] and p[X] < wall[X] + wall[W] and p[Y] + hitbox[H] >= wall[Y] and p[Y] + wall[H] + vPlayer[Y] > wall[Y]:
    #         vPlayer[BOT] = wall[Y]
    #         p[Y] = vPlayer[BOT] - hitbox[H]
    #         vPlayer[Y] = 0

                    


            


def checkBorders(p, hitbox, vPlayer, borders): #fix movement here
    for b in borders[0]:

        if (p[X] + 5) + hitbox[W] == b[X]:
            vPlayer[X] = 0
            p[X] = b[X] - 5 - hitbox[W]
            p[Y] = vPlayer[BOT] - hitbox[H]

        elif p[X] - 5 == b[X] + b[W]:
            vPlayer[X] = 0 
            p[X] = b[X] + b[W] + 5
            p[Y] = vPlayer[BOT] - hitbox[H]

        if p[X] + hitbox[W] > b[X] and p[X] < b[X] + b[W] and p[Y] + hitbox[H] >= b[Y] and p[Y] + hitbox[H] + vPlayer[Y] > b[Y]:
            vPlayer[BOT] = b[Y]
            p[Y] = vPlayer[BOT] - hitbox[H]
            vPlayer[Y] = 0

    for b in borders[1]:

        if (p[X] + 5) + hitbox[W] == b[X]:
            vPlayer[X] = 0
            p[X] = b[X] - 5

        elif p[X] - 5 == b[X] + b[W]:
            vPlayer[X] = 0 
            p[X] = b[X] + b[W] + 5

        if Rect(p[X], p[Y], hitbox[W], hitbox[H]).colliderect(b):
            vPlayer[TOP] = b[Y] + b[H]
            p[Y] = vPlayer[TOP]
            if p[Y] > b[H] + b[Y]:
                vPlayer[Y] = 0


def hitSpikes(x, y, hitbox ,spikes):
    collisionList = []
    for spike in spikes:
        playerRect = Rect(x, y, hitbox[W], hitbox[H])
        return playerRect.collidelist(spike)

def healthBar(health, pics):
    for i in range(3):
        if i == health:
            pic = pics[i]
            return pic