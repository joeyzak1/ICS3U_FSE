#shortcutFunctions.py
# this program has useful functions that can shorten code
from pygame import *

screen = display.set_mode((1024, 768))

jumpSpeed = -20; gravity = 1

X = 0; Y = 1; W = 2; H = 3; BOT = 2; SCREENX = 3; ROW = 2; COL = 3; TOP = 4

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

def drawSlugs(slugs):
    'this function draws slugs - work on these LATER'
    return 1 

def drawBorders (borders, offset):
    'this function draws borders'
    for border in borders:
        border = border.move(offset, 0)
        draw.rect(screen, (255, 0, 0), border)

def createHitbox (pic, x, y):
    'this function creates a hitbox'
    pic_width = pic.get_width()
    pic_height = pic.get_height()
    hitbox = Rect (x, y, pic_width, pic_height)
    return hitbox

def playerSprites (player, sprites, vPlayer):
    'this function gets the sprite of a character'
    row = player[ROW]
    col = int(player[COL])
    pic = sprites[row][col]
    pictureRect = createHitbox(pic, vPlayer[SCREENX], player[Y])
    screen.blit(pic, pictureRect)
    return pictureRect

def checkPlats(plats, p, vPlayer):
    for plat in plats:
        if p[X] + p[W] > plat[X] and p[X] < plat[X] + plat[W] and p[Y] + p[H] <= plat[Y] and p[Y] + p[H] + vPlayer[Y] > plat[Y]:
            vPlayer[BOT] = plat[Y]
            p[Y] = vPlayer[BOT] - p[H]
            vPlayer[Y] = 0


def moveGuyLeft(p, vPlayer):
    'this function moves the guy to the left'
    keys = key.get_pressed()
    p[ROW] = 3
    vPlayer[X] = -5
    if keys[K_LSHIFT] or keys[K_RSHIFT]:
        vPlayer[X] = -10
    if vPlayer[SCREENX] > 250:
        vPlayer[SCREENX] -= 5

def moveGuyRight(p, vPlayer):
    'this function moves the guy to the right'
    keys = key.get_pressed()
    p[ROW] = 4
    vPlayer[X] = 5
    if keys[K_LSHIFT] or keys[K_RSHIFT]:
        vPlayer[X] = 10
    if vPlayer[SCREENX] < 700:
        vPlayer[SCREENX] += 5
