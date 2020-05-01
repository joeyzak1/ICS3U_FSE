from pygame import *
from shortcutFunctions import *

#MUSIC
# init()
# file='clipOne.mp3'
# mixer.music.load(file)
# mixer.music.play(-1)

size = width, height = 1024, 768
screen = display.set_mode(size)

backPic = image.load("Level One/background_levelOne.png") #background


GROUND = 677; bottom = GROUND #ground and jump variables for jumping, platforms, etc.
jumpSpeed = -20; gravity = 1

X = 0; Y = 1; W = 2; H = 3; BOT = 2; SCREENX = 3; ROW = 2; COL = 3; TOP = 4 #variables for navigating around lists

v = [0, 0, bottom, 512, 0] #velocity of player

v_bull = [-5, 0] #vel of bullets

v_bird = [0, 0]; vBird_vertical = 30; vBrid_gravity = -1 #velocity of birds

plats = [Rect(900, 525, 200, 15), Rect(3000, 460, 200, 15), Rect(5000, 530, 200, 15), Rect(5400, 450, 200, 15), Rect(6300, 525, 200, 15),
        Rect(6600, 400, 200, 15), Rect(6900, 275, 200, 15)] #platform rect list

blocks = [Rect(1150, 360, 250, 40), Rect(3900, 75, 50, 300), Rect(3950, 75, 200, 50), Rect(4100, 75, 50, 150), Rect(3900, 187, 75, 150),
        Rect(4250, 75, 50, 300), Rect(4250, 325, 200, 50), Rect(4400, 375, 50, -300), Rect(4550, 75, 50, 300), Rect(7200, 175, 250, 40)] #blocks rect list

squared_blocks = [Rect(1250, 182, 50, 50), Rect(5475, 250, 50, 50)] #squared blocks rect list

slugs = [Rect(2050, 645, 30, 30), Rect(3600, 602, 30, 30), Rect(5700, 645, 30, 30)] #slugs rect list

birds = [Rect(3300, 50, 50, 15), Rect(5300, 50, 50, 15)] #rect list for birds
bird_p = [[birds[i][X], birds[i][Y], 0] for i in range(len(birds))]
bird_hitboxes = []

# print (bird_p)

borders = [Rect(2732, 632, 1366, 47)] #ground border

doorRect = Rect(7305, 100, 40, 75) #rect for door

rapid = 100; sword = 20 #for speed of bullets and sword

isJump = False #variable for checking jumps

health = 2



def drawScene(screen, p, sprites, player, plats, blocks, sqblocks, slugs, b_slugs, birds, b_s, sprites_b, borders, door, hearts, health):
    global rapid

    offset = v[SCREENX]-p[X] #offset to move screen with eveything
    screen.blit(backPic, (offset, 0)) #background


    for plat in plats: #this for loop blits all platforms in the correct position
        plat = plat.move(offset, 0)
        draw.rect(screen, (0), plat)
    # drawPlats(plats)

    for block in blocks: #this loop blits all blocks
        block = block.move(offset, 0)
        draw.rect(screen, (255, 0, 0), block)

    for sq in sqblocks: #this for loop blits all squared blocks
        sq = sq.move(offset, 0)
        draw.rect(screen, (0, 0, 255), sq)

    for slug in slugs: #this blits the slugs
        slug = slug.move(offset, 0); draw.rect(screen, (0, 255, 255), slug)

        if rapid < 100 and p[X] + 500 <= slug[X]: #checking for bullet speed
            rapid += 1

        if slug[0] <= 1400 and rapid == 100 and p[X] + 500 <= slug[X]: #checking if bullet speed is slow enough to shoot
            b_slugs.append([slug[0], 645, v_bull[0], v_bull[1]])
            rapid = 0

    for b in b_slugs: #bullets
        bs_rect = Rect(b[0], b[1], 20, 10)
        draw.rect(screen, (255, 255, 0), bs_rect)

    # for bird in birds:
    #     for sp in b_s:
    #         bird = bird.move(offset, 0)
    #         row = int(sp[ROW])
    #         pic_b = sprites_b[row]
    #         b_s_width = pic_b.get_width(); b_s_height = pic_b.get_height()
    #         hitbox_b = Rect(bird[X], bird[Y], b_s_width, b_s_height)


    #         draw.rect(screen, (255, 0, 120), hitbox_b, 2)
    #         screen.blit(pic_b, hitbox_b)

    for b in b_s: #birds
        # b = b.move(offset, 0)
        row = int(b[ROW])
        print (row)
        if row > 4:
            row = 0
        pic_bird = sprites_b[row]

        # get_hitbox(pic_bird, b)

        # bird_width = pic_bird.get_width()
        # bird_height = pic_bird.get_height()
        # birdHitbox = Rect(b[X], b[Y], bird_width, bird_height)
        # birdHitbox = birdHitbox.move(offset, 0)
        # bird_hitboxes.append(birdHitbox)

        screen.blit(pic_bird, createHitbox(pic_bird, b[X], b[Y]).move(offset, 0))
        draw.rect(screen, (255, 0, 0), createHitbox(pic_bird, b[X], b[Y]).move(offset, 0), 1)

        # screen.blit(pic_bird, get_hitbox(pic_bird, b))

    for border in borders:
        border = border.move(offset, 0)
        draw.rect(screen, (255, 0, 0), border, 3)

    #health
    screen.blit(healthBar(health, hearts), (0, 0))

    door = door.move(offset, 0)
    draw.rect(screen, (123, 213, 7), door)

    row = player[ROW]
    col = int(player[COL])
    pic = sprites[row][col]
    # sprite_width = pic.get_width()
    # sprite_height = pic.get_height()

    # hitBox = Rect(v[SCREENX], p[1], sprite_width, sprite_height)
    screen.blit(pic, createHitbox(pic, v[SCREENX], p[Y]))
    draw.rect(screen, (255, 0, 0), createHitbox(pic, v[SCREENX], p[Y]), 2)



def healthBar(health, pics):
    for i in range(3):
        if i == health:
            pic = pics[i]
            return pic




def move(p, player, sprites, blocks, birds):

    keys = key.get_pressed()
    mx, my = mouse.get_pos()


    if keys[K_SPACE] and p[Y] + p[H] == v[BOT] and v[Y] == 0: #fix this area
        v[Y] = jumpSpeed


    # if keys[K_x]:
    #     player[ROW] = 0
    #     if player[COL] >= len(sprites[0]):
    #         player[COL] = 0


    if keys[K_LEFT] and p[X] > 400 and hitBlocks(p[X]-5, p[Y], blocks) and hitBlocks(p[X]-5, p[Y], squared_blocks):
        player[ROW] = 3

        if p[X] + 5 < 7550:

            if keys[K_LSHIFT] or keys[K_RSHIFT]:
                v[X] = -10

            else:
                v[X] = -5

            if v[SCREENX] > 350:
                v[SCREENX] -= 5


        elif p[X] > 7550:
            if v[X] == 0:
                if keys[K_LSHIFT] or keys[K_RSHIFT]:
                    v[X] = -10

                else:
                    v[X] = -5


        #     v[X] = 0
            # v[SCREENX] = 0




    elif keys[K_RIGHT] and p[X] < 12280 and hitBlocks(p[X]+5, p[Y], blocks) and hitBlocks(p[X]+5, p[Y], squared_blocks):
        player[ROW] = 4


        if p[X] + 5 < 7550:

            if keys[K_LSHIFT] or keys[K_RSHIFT]:
                v[X] = 10
            else:
            # p[ROW] = 4
                v[X] = 5

            if v[SCREENX] < 700:
                v[SCREENX] += 5

        elif p[X] > 7550:
            player[COL] = 0
            if v[X] > 0:
                v[X] = 0
        #     v[X] = 0
            # v[SCREENX] = 0


    

    else:
        player[COL] = 0
        player[COL] -= 0.2
        v[X] = 0


    player[COL] += 0.2


    if player[COL] >= len(sprites[ROW]):
        player[COL] = 1



    p[X] += v[X]
    v[Y] += gravity

    # print(p[X])







def move_bird(p, birds, bird_p, sprites):
    # for bird in birds:
    for b in bird_p:
        
        if p[X] + 400 >= b[X]:

            v_bird[Y] = vBird_vertical
            v_bird[X] = -15

            if b[X] <= p[X] + 200 and b[Y] >= p[Y]:
                v_bird[Y] = 0



        # else:
        #     b[ROW] = 0
        #     b[ROW] -= 0.2

            # if b[ROW] == 5:
            #     b[ROW] = 0


            b[ROW] += 0.2
            
            b[Y] += v_bird[Y]
            b[X] += v_bird[X]






def move_slugBullets(bull):
    for b in bull:
        b[0] += b[2]
        b[1] == b[3]
        if b[0] < 0:
            bull.remove(b)





def move_bad(p, bull, birds, bird_p, sprite_bird):
    move_slugBullets(bull)
    move_bird(p, birds, bird_p, sprite_bird)








def check(p, plats, borders, birds, birdHitboxes):
    global isJump

    keys = key.get_pressed()

    if v[Y] != v[BOT]:
        isJump = True

    if p[Y] + p[H] >= GROUND:
        isJump = False

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

    for block in blocks:
        if isJump and Rect(p[X], p[Y]-5, p[W], p[H]).colliderect(block):
            v[TOP] = block[Y] + block[H]
            p[Y] = v[TOP]
            v[Y] += gravity

        if isJump and Rect(p[X], p[Y] + 5, p[W], p[H]).colliderect(block):
            v[BOT] = block[Y]
            p[Y] = v[BOT] - p[H]

            if keys[K_SPACE]: #these next 2 sections are for fixing issues with not being able to jump on blocks
                v[Y] = jumpSpeed

            else:
                v[Y] = 0

    for sq in squared_blocks:
        if isJump and Rect(p[X], p[Y]-5, p[W], p[H]).colliderect(sq):
            v[TOP] = sq[Y] + sq[H]
            p[Y] = v[TOP]
            v[Y] += gravity

        if isJump and Rect(p[X], p[Y] + 5, p[W], p[H]).colliderect(sq):
            v[BOT] = sq[Y]
            p[Y] = v[BOT] - p[H]

            if keys[K_SPACE]: #these next 2 sections are for fixing issues with not being able to jump on blocks
                v[Y] = jumpSpeed

            else:
                v[Y] = 0

    # check_bird(p, birds, birdHitboxes)
    birdCollision(p, birds)




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

# def check_bird(p, birds, hitboxes):
#     for bird in birds:
#         for hitbox in hitboxes:
#             if hitbox.colliderect(p):
#                 birds.remove(bird)
#                 hitboxes.remove(hitbox)

def birdCollision(p, birds):
    global health 
    
    for bird in birds:
        birdRect = Rect(bird[X], bird[Y], 100, 80)
        if birdRect.colliderect(p):
            birds.remove(bird)
            health -= 1


def hitBlocks(x, y, blocks):
    playerRect = Rect(x, y, 35, 50)
    return playerRect.collidelist(blocks)