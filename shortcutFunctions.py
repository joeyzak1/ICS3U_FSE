#shortcutFunctions.py
# this program has useful functions that can shorten code
from pygame import *

screen = display.set_mode((1024, 768))

jumpSpeed = -20; gravity = 1

X = 0; Y = 1; W = 2; H = 3; BOT = 2; SCREENX = 3; ROW = 2; COL = 3; TOP = 4

vel_bird = [0, 0]
vBird_vertical = 30
vBrid_gravity = -1

def drawPlats(plats, offset):
    'this function draws platforms with offset. the platforms must be in a LIST, and must be Rect objects'
    # global offset
    for plat in plats:
        plat = plat.move(offset, 0)
        draw.rect(screen, (0), plat)

def drawSpikes(spikes, offset):
    for sp in spikes:
        for ground in sp:
            ground = ground.move(offset, 0)
            draw.rect(screen, (0, 255, 0), ground)

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
            draw.rect(screen, (255, 0, 0), border)

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

def playerSprites (player, p, sprites, vPlayer):
    'this function gets the sprite of a character'
    row = player[ROW]
    col = int(player[COL])
    pic = sprites[row][col]
    pictureRect = createHitbox(pic, vPlayer[SCREENX], p[Y])
    screen.blit(pic, pictureRect)
    return pictureRect

def checkPlats(plats, p, hitBox, vPlayer):
    for plat in plats:
        if p[X] + hitBox[W] > plat[X] and p[X] < plat[X] + plat[W] and p[Y] + hitBox[H] <= plat[Y] and p[Y] + hitBox[H] + vPlayer[Y] > plat[Y]:
            vPlayer[BOT] = plat[Y]
            p[Y] = vPlayer[BOT] - hitBox[H]
            vPlayer[Y] = 0

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


def moveBird(player, birds):
    for bird in birds:
        if player[X] + 400 >= bird[X]:
            vel_bird[Y] = vBird_vertical
            vel_bird[X] = -15

            if bird[X] <= player[X] + 200 and bird[Y] >= player[Y]:
                vel_bird[Y] = 0

            bird[Y] += vel_bird[Y]
            bird[X] += vel_bird[X]

def checkSpikes(p, hitbox, spikes, vPlayer):
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