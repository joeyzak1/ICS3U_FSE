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
    'this function draws platforms with offset. the platforms must be in a LIST, and must be Rect objects'
    # global offset
    for plat in plats:
        plat = plat.move(offset, 0)
        screen.blit(pic, (plat[X], plat[Y]))

def drawSpikes(spikes, offset):
    'this functions draws spikes'
    for sp in spikes:
        for ground in sp: #went through two loops to get to desired spikes (2d list)
            ground = ground.move(offset, 0)
            # draw.rect(screen, (0, 255, 0), ground)

def drawBlocks(blocks):
    'this function draws blocks - blocks must be in a LIST and have offset'
    for block in blocks: #this loop blits all blocks
        block = block.move(offset, 0)
        draw.rect(screen, (255, 0, 0), block)

def drawSqBlocks(sq_blocks):
    'this function draws squared blocks - param needs to be a list'
    for sq in sq_blocks: #this for loop blits all squared blocks
        sq = sq.move(offset, 0)
        draw.rect(screen, (0, 0, 255), sq)

def drawHealthBlocks(healthB, offset):
    for h in healthB:
        h = h.move(offset, 0)
        draw.rect(screen, (0, 0, 255), h)

def drawSlugs(slugs):
    'this function draws slugs - work on these LATER'
    return 1 

def drawBorders (borders, offset):
    'this function draws borders'
    for lists in borders:
        for border in lists:
            border = border.move(offset, 0)

def drawTempBird(birds, offset):
    for bird in birds:
        bird = bird.move(offset, 0)
        draw.rect(screen, (120, 255, 89), [bird[X], bird[Y], 60, 30])

def createHitbox (pic, x, y):
    'this function creates a hitbox'
    pic_width = pic.get_width()
    pic_height = pic.get_height()
    hitbox = Rect (x, y, pic_width, pic_height)
    return hitbox

def playerSprites (player, p, sprites, vPlayer, x):
    'this function gets the sprite of a character'
    row = player[ROW]
    col = int(player[COL])
    if row == 0 and col == 5:
        col = 0
    pic = sprites[row][col]
    pictureRect = createHitbox(pic, x, p[Y])
    screen.blit(pic, pictureRect)
    return pictureRect

# boss bullets --------------------------------------------------
def drawBossBullets(bullets):
    for b in bullets:
        draw.circle(screen, (0, 255, 0), (int(b[0]),int(b[1])), 4)

def createBossBullets(bullets, SPEED, bossR, rapid):
    for i in range(12):
        ang = atan2(bossR[Y] - 318, bossR[X] - 424)
        ang *= i
        vx = cos(ang)*SPEED #horizontal component
        vy = sin(ang)*SPEED #vertical component

        bullets.append([bossR[X], bossR[Y], vx, vy])   
    

def checkBossBullets(bullets):
    for b in bullets[:]: #[:] is a COPY of the bullets list
        b[0] += b[2]
        b[1] += b[3]

        if b[0] > 978 or b[0] < 46 or b[1] < 0: #off screen
            bullets.remove(b)

#move boss between attacks ------------------------------------
def moveBossBetween(boss, b, v):
    v[X] = 0
    for i in range(2):
        if b[X] > 550:
            v[X] = -3

        elif 600 < b[X] < 625:
            v[X] = 3

#move boss close to player
def moveBossPhaseTwo(boss, b, v, player, p):
    if b[X] <= p[X] + p[H]:
        v[X] = 0
        v[Y] = 15
    else:
        v[Y] = -4
        v[X] = -4







def checkPlats(plats, p, player, hitBox, v):
    # for plat in plats:
    #     if p[X] + hitBox[W] > plat[X] and p[X] < plat[X] + plat[W] and p[Y] + hitBox[H] <= plat[Y] and p[Y] + hitBox[H] + vPlayer[Y] > plat[Y]:
    #         vPlayer[BOT] = plat[Y]
    #         p[Y] = vPlayer[BOT] - hitBox[H]
    #         player[Y] = vPlayer[BOT] - hitBox[H]
    #         vPlayer[Y] = 0
    for plat in plats:
        if p[X] + p[W] > plat[X] and p[X] < plat[X] + plat[W] and p[Y] + p[H] <= plat[Y] and p[Y] + p[H] + v[Y] > plat[Y]:
            v[BOT] = plat[Y]
            p[Y] = v[BOT] - p[H]
            v[Y] = 0





def moveGuyLeft(p, player, vPlayer, leftEnd, rightEnd):
    'this function moves the guy to the left'
    keys = key.get_pressed()

    if leftEnd < p[X] + 5 < rightEnd:
        player[ROW] = 3
        vPlayer[X] = -5
        if keys[K_LSHIFT] or keys[K_RSHIFT]:
            vPlayer[X] = -10
        if vPlayer[SCREENX] > 250:
            vPlayer[SCREENX] -= 5

    elif p[X] > rightEnd:
        if vPlayer[X] == 0:
            if keys[K_LSHIFT] or keys[K_RSHIFT]:
                vPlayer[X] = -10
            else:
                vPlayer[X] = -5


def moveGuyRight(p, player, vPlayer, leftEnd, rightEnd):
    'this function moves the guy to the right'
    keys = key.get_pressed()

    if leftEnd < p[X] + 5 < rightEnd:
        player[ROW] = 4
        vPlayer[X] = 5
        if keys[K_LSHIFT] or keys[K_RSHIFT]:
            vPlayer[X] = 10
        if vPlayer[SCREENX] < 700:
            vPlayer[SCREENX] += 5

    elif p[X] > rightEnd:
        player[COL] = 0
        if vPlayer[X] > 0:
            vPlayer[X] = 0

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


def moveBird(player, birds):
    for bird in birds:
        if player[X] + 400 >= bird[X]:
            vel_bird[Y] = vBird_vertical
            vel_bird[X] = -15

            if bird[X] <= player[X] + 200 and bird[Y] >= player[Y]:
                vel_bird[Y] = 0

            bird[Y] += vel_bird[Y]
            bird[X] += vel_bird[X]

def checkSpikes(p, hitbox, spikes, vPlayer, health):
    for spike in spikes:
        for sp in spike:
            if Rect(p[X], p[Y], hitbox[W], hitbox[H]).colliderect(sp):
                health -= 1
                if health < 0:
                    health = 0
            
    for grnd in spikes[0]:
        # if p[X] + 5 + hitbox[W] == grnd[X]:
        #     vPlayer[X] = 0
        #     p[X] = grnd[X] - 5 - hitbox[W]
        #     p[Y] = vPlayer[BOT] - hitbox[H]

        # elif p[X] - 5 + hitbox[W] == grnd[X]:
        #     vPlayer[X] = 0
        #     p[X] = grnd[X] + grnd[W] + 5
        #     p[Y] = vPlayer[BOT] - hitbox[H]

        if p[X] + hitbox[W] > grnd[X] and p[X] < grnd[X] + grnd[W] and p[Y] + hitbox[H] >= grnd[Y] and p[Y] + hitbox[H] + vPlayer[Y] > grnd[Y]:

            vPlayer[BOT] = grnd[Y]
            p[Y] = vPlayer[BOT] - hitbox[H]
            vPlayer[Y] = 0
            

    for air in spikes[1]:
        # if p[X] + 5  + hitbox[W] == air[X]:
        #     vPlayer[X] = 0
        #     p[X] = air[X] - 5

        # elif p[X] - 5 == air[X] + air[W]:
        #     vPlayer[X] = 0 
        #     p[X] = air[X] + air[W] + 5
        #     p[Y] = vPlayer[BOT] - hitbox[H]

        if Rect(p[X], p[Y], hitbox[W], hitbox[H]).colliderect(air):
            vPlayer[TOP] = air[Y] + air[H]
            p[Y] = vPlayer[TOP]
            if p[Y] > air[H] + air[Y]:
                vPlayer[Y] = 0

    for wall in spikes[2]:
        if p[X] + hitbox[W] > wall[X] and p[X] < wall[X] + wall[W] and p[Y] + hitbox[H] >= wall[Y] and p[Y] + wall[H] + vPlayer[Y] > wall[Y]:
            vPlayer[BOT] = wall[Y]
            p[Y] = vPlayer[BOT] - hitbox[H]
            vPlayer[Y] = 0

                    


            


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
        collisionList.append(playerRect.collidelist(spike))

    return collisionList[-1]

def healthBar(health, pics):
    for i in range(3):
        if i == health:
            pic = pics[i]
            return pic