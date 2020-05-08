#shortcutFunctions.py
# this program has useful functions that can shorten code
from pygame import *
# import main
# from levelOne import *
# from main import *

# vscreenX = 512
# offset = vscreenX - main.p[X]

jumpSpeed = -20; gravity = 1

X = 0; Y = 1; W = 2; H = 3; BOT = 2; SCREENX = 3; ROW = 2; COL = 3; TOP = 4

def drawPlats(plats):
    'this function draws platforms with offset. the platforms must be in a LIST, and must be Rect objects'
    global offset
    for plat in plats:
        plat = plat.move(offset, 0)
        draw.rect(screen, (0), plat)

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

def drawBorders (borders):
    for border in borders:
        border = border.move(offset, 0)
        draw.rect(screen, (255, 0, 0), border)

def createHitbox (pic, x, y):
    pic_width = pic.get_width()
    pic_height = pic.get_height()
    hitbox = Rect (x, y, pic_width, pic_height)
    return hitbox