from pygame import *

size = width, height = 1024, 768
screen = display.set_mode(size)

backPic = image.load("Level One/background_levelOne.png")


GROUND = 677; bottom = GROUND
jumpSpeed = -20; gravity = 1

X = 0; Y = 1; W = 2; H = 3; BOT = 2; SCREENX = 3; ROW = 2; COL = 3

v = [0, 0, bottom, 512]

plats = [Rect(900, 525, 200, 15)]
blocks = [Rect(1150, 350, 250, 40)]



def drawScene(screen, p, plats, blocks):
    offset = v[SCREENX]-p[X]
    screen.blit(backPic, (offset, 0))

    for plat in plats:
        plat = plat.move(offset, 0)
        draw.rect(screen, (0), plat)

    for block in blocks:
        block = block.move(offset, 0)
        draw.rect(screen, (255, 0, 0), block)

    draw.rect(screen, (0), [v[SCREENX], p[1], p[2], p[3]])
    # row = p[ROW]
    # col = int(p[COL])
    # pic = picList[row][col]
    # screen.blit(pic, (p[X], p[Y]))


def move(p):
    keys = key.get_pressed()

    if keys[K_SPACE] and p[Y] + p[H] == v[BOT] and v[Y] == 0: #fix this area
        if v[Y] > 0 and hitBlocks(p[X], p[Y] + 5, blocks) \
        or v[Y] < 0  and hitBlocks(p[X], p[Y] + 5, blocks):
            v[Y] = jumpSpeed

    if keys[K_LEFT] and p[X] > 400 and hitBlocks(p[X]-5, p[Y], blocks):
        if keys[K_LSHIFT] or keys[K_RSHIFT]:
            v[X] = -10

        else:
        # p[ROW] = 3
            v[X] = -5

        if v[SCREENX] > 350:
            v[SCREENX] -= 5


    elif keys[K_RIGHT] and p[X] < 12280 and hitBlocks(p[X]+5, p[Y], blocks):
        if keys[K_LSHIFT] or keys[K_RSHIFT]:
            v[X] = 10
        else:
        # p[ROW] = 4
            v[X] = 5
        if v[SCREENX] < 700:
            v[SCREENX] += 5

    else:
        # p[COL] = 0
        v[X] = 0

    # p[COL] = p[COL]+0.2

    # if p[COL] >= len(pics[ROW]):
    #     p[COL] = 1

    p[X] += v[X]
    v[Y] += gravity


def check(p, plats):
    for plat in plats:
        if p[X] + p[W] > plat[X] and p[X] < plat[X] + plat[W] and p[Y] + p[H] <= plat[Y] and p[Y] + p[H] + v[Y] > plat[Y]:
            v[BOT] = plat[Y]
            p[Y] = v[BOT] - p[H]
            v[Y] = 0


    p[Y] += v[Y]

    if p[Y] + p[H] >= GROUND:
        v[BOT] = GROUND
        p[Y] = GROUND-p[H]
        v[Y] = 0

def hitBlocks(x, y, blocks):
    playerRect = Rect(x, y, 35, 50)
    return playerRect.collidelist(blocks)





