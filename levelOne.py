from pygame import *

size = width, height = 1024, 768
screen = display.set_mode(size)

backPic = image.load("Level One/background_levelOne.png")


GROUND = 677; bottom = GROUND
jumpSpeed = -20; gravity = 1

X = 0; Y = 1; W = 2; H = 3; BOT = 2; SCREENX = 3; ROW = 2; COL = 3

v = [0, 0, bottom, 512]

def drawScene(screen, p, picList):
    offset = v[SCREENX]-p[X]
    screen.blit(backPic, (offset, 0))

    # draw.rect(screen, (0), [v[SCREENX], p[1], p[2], p[3]])
    row = p[ROW]
    col = int(p[COL])
    pic = picList[row][col]
    screen.blit(pic, (p[X], p[Y]))


def move(p, pics):
    keys = key.get_pressed()

    if keys[K_SPACE] and p[Y] + p[H] == v[BOT] and v[Y] == 0:
        v[Y] = jumpSpeed


    if p[Y] != bottom:
        p[ROW] = 2

    if keys[K_LEFT] and p[X] > 400:
        p[ROW] = 3
        v[X] = -5

        if v[SCREENX] > 100:
            v[SCREENX] -= 5


    elif keys[K_RIGHT] and p[X] < 12280:
        p[ROW] = 4
        v[X] = 5
        if v[SCREENX] < 900:
            v[SCREENX] += 5

    else:
        p[COL] = 0
        v[X] = 0

    p[COL] = p[COL]+0.2

    if p[COL] >= len(pics[ROW]):
        p[COL] = 1

    p[X] += v[X]
    v[Y] += gravity


def check(p):
    p[Y] += v[Y]

    if p[Y] + p[H] >= GROUND:
        v[BOT] = GROUND
        p[Y] = GROUND-p[H]
        v[Y] = 0


