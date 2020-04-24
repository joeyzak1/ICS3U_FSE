from pygame import *
from tkinter import *

size = width, height = 1024, 768
screen = display.set_mode(size)

backPic = image.load("Level One/background_levelOne.png")


GROUND = 677; bottom = GROUND
jumpSpeed = -20; gravity = 1

X = 0; Y = 1; W = 2; H = 3; BOT = 2; SCREENX = 3; ROW = 2; COL = 3

v = [0, 0, bottom, 512]
v_bull = [-5, 0]

plats = [Rect(900, 525, 200, 15), Rect(3000, 460, 200, 15), Rect(5000, 530, 200, 15), Rect(5400, 450, 200, 15)]
blocks = [Rect(1150, 360, 250, 40), Rect(3900, 75, 50, 300), Rect(3950, 75, 200, 50), Rect(4100, 75, 50, 150), Rect(3900, 187, 75, 150),
        Rect(4250, 75, 50, 300), Rect(4250, 325, 200, 50), Rect(4400, 375, 50, -300), Rect(4550, 75, 50, 300)]

rotated_R = Surface((75, 150))
rotated_R.fill((255, 0, 0 ))
rotated_R = transform.rotate(rotated_R, 315)
screen.blit(rotated_R, blocks[4])

squared_blocks = [Rect(1250, 182, 50, 50), Rect(5475, 250, 50, 50)]
slugs = [Rect(2050, 645, 30, 30), Rect(3600, 602, 30, 30), Rect(5700, 645, 30, 30)]
birds = [Rect(3300, 50, 50, 15), Rect(5300, 50, 50, 15)]
borders = [Rect(2732, 632, 1366, 47)]

rapid = 20; sword = 20



def drawScene(screen, p, sprites, player, plats, blocks, sqblocks, slugs, b_slugs, birds, borders):
    global rapid
    offset = v[SCREENX]-p[X]
    screen.blit(backPic, (offset, 0))


    for plat in plats:
        plat = plat.move(offset, 0)
        draw.rect(screen, (0), plat)

    for block in blocks:
        block = block.move(offset, 0)
        draw.rect(screen, (255, 0, 0), block)

    for sq in sqblocks:
        sq = sq.move(offset, 0)
        draw.rect(screen, (0, 0, 255), sq)

    for slug in slugs:
        slug = slug.move(offset, 0); draw.rect(screen, (0, 255, 255), slug)

        if rapid < 20:
            rapid += 1

        if slug[0] <= 1400 and rapid == 20:
            b_slugs.append([slug[0], 645, v[0], v[1]])
            rapid = 0

    for b in b_slugs:
        bs_rect = Rect(b[0], b[1], 20, 10)
        draw.rect(screen, (255, 255, 0), bs_rect)

    for bird in birds:
        bird = bird.move(offset, 0)
        draw.rect(screen, (255, 0, 120), bird)

    for border in borders:
        border = border.move(offset, 0)
        draw.rect(screen, (255, 0, 0), border, 3)

    row = player[ROW]
    col = int(player[COL])
    pic = sprites[row][col]
    sprite_width = pic.get_width()
    sprite_height = pic.get_height()

    hitBox = Rect(v[SCREENX], p[1], sprite_width, sprite_height)
    screen.blit(pic, hitBox)
    draw.rect(screen, (255, 0, 0), hitBox, 2)

    # print(row, col)
    # print(p[X])



    # draw.rect(screen, (0), [v[SCREENX], p[1], p[2], p[3]])
    # row = p[ROW]
    # col = int(p[COL])
    # pic = picList[row][col]
    # screen.blit(pic, (p[X], p[Y]))


def move(p, player, sprites):
    keys = key.get_pressed()
    mx, my = mouse.get_pos()

    if keys[K_SPACE] and p[Y] + p[H] == v[BOT] and v[Y] == 0: #fix this area
        v[Y] = jumpSpeed

        if hitBlocks(p[X], p[Y] - 5, blocks):
            v[Y]  = jumpSpeed

        elif hitBlocks(p[X], p[Y] + 5, blocks):
            v[Y] += gravity

    if v[Y] == jumpSpeed or v[Y] < 0:
        player[ROW] = 2




    if keys[K_LEFT] and p[X] > 400 and hitBlocks(p[X]-5, p[Y], blocks):
        player[ROW] = 3
        if keys[K_LSHIFT] or keys[K_RSHIFT]:
            v[X] = -10

        else:
            v[X] = -5

        if v[SCREENX] > 350:
            v[SCREENX] -= 5


    elif keys[K_RIGHT] and p[X] < 12280 and hitBlocks(p[X]+5, p[Y], blocks):
        player[ROW] = 4

        if keys[K_LSHIFT] or keys[K_RSHIFT]:
            v[X] = 10
        else:
        # p[ROW] = 4
            v[X] = 5

        if v[SCREENX] < 700:
            v[SCREENX] += 5


    # else:
    #     player[COL] = 0
    #     player[COL] -= 0.2
    #     v[X] = 0


    # if keys[K_x]:
    #     player[ROW] = 0
    #     check_attack(p, slugs, birds)
    #     if player[COL] >= 4:
    #         player[COL] = 0

    else:
        player[COL] = 0
        player[COL] -= 0.2
        v[X] = 0

    player[COL] += 0.2


    if player[COL] >= len(sprites[ROW]):
        player[COL] = 0

    p[X] += v[X]
    v[Y] += gravity



def move_slugBullets(bull):
    for b in bull:
        b[0] += b[2]
        b[1] == b[3]
        if b[0] < 0:
            bull.remove(b)



def check(p, plats, borders):
    for plat in plats:
        if p[X] + p[W] > plat[X] and p[X] < plat[X] + plat[W] and p[Y] + p[H] <= plat[Y] and p[Y] + p[H] + v[Y] > plat[Y]:
            v[BOT] = plat[Y]
            p[Y] = v[BOT] - p[H]
            v[Y] = 0

    for border in borders:
        if p[X]+5 + p[W] > border[X] and p[X] < border[X] + border[W]  and v[BOT] == GROUND:
            v[X] = 0

        if p[X] + p[W] > border[X] and p[X] < border[X] + border[W] and p[Y] + p[H] >= border[Y] and p[Y] + p[H] + v[Y] > border[Y]:
            v[BOT] = border[Y]
            p[Y] = v[BOT] - p[H]
            v[Y] = 0


    p[Y] += v[Y]

    if p[Y] + p[H] >= GROUND:
        v[BOT] = GROUND
        p[Y] = GROUND-p[H]
        v[Y] = 0

def check_bullSlug(bull, p):
    for b in bull:
        bullS_Rect = Rect(b[0], b[1], 20, 10)
        if bullS_Rect.colliderect(p):
            bull.remove(b)
            break

def check_attack(p, slugs, birds):
    for slug in slugs:
        for bird in birds:
            if p.colliderect(slug):
                slugs.remove(slug)

            elif p.colliderect(bird):
                birds.remove(bird)


def hitBlocks(x, y, blocks):
    playerRect = Rect(x, y, 35, 50)
    return playerRect.collidelist(blocks)












