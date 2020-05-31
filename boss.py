#boss.py

from pygame import *
import shortcutFunctions

screen = display.set_mode((1024, 768))
myClock = time.Clock()

backPic = image.load('Backgrounds/bossBack.png').convert()

#standard variables
X = 0
Y = 1
W = 2
H = 3
ROW = 2
COL = 3
BOT = 2

GROUND = 722
bottom = GROUND

jumpSpeed = -20
gravity = 1

#player objects
player = [150, 650, 4, 0]
pRect = Rect(150, 650, 20, 45)

#boss objects
boss = [600, 330, 0, 0]
bossRect = Rect(600, 330, 386, 392)

direction = -1 #direction of movement of the boss

vPlayer = [0, 0, bottom] #v for player
vBoss = [0, 0, bottom, direction] #v for boss

#for bullets
bullSpeed = 5
bullets = []
rapid = 50
playerBullets = []

#time
myTime = 0
timePassed = []

bossHealth = 30
visible = True

def drawScene(p, player, sprites, boss, b, bullets, bossSprites, timeFont, playerBullets):
    'This function draws the scene'
    global vPlayer
    global myTime
    global timePassed
    global vBoss
    global bossHealth
    # global visible

    #same few lines as previous files
    screen.blit(backPic, (0, 0))

    shortcutFunctions.playerSprites(player, p, sprites, vPlayer, p[X])
    hitbox = shortcutFunctions.playerSprites(player, p, sprites, vPlayer, p[X])


    if visible:
        shortcutFunctions.playerSprites(boss, b, bossSprites, vBoss, b[X])

    for bull in bullets: #go through the bullets list
        draw.circle(screen, (0, 255, 0), (int(bull[0]),int(bull[1])), 4) #draw the bullet

    for bull in playerBullets:
        bullRect = Rect(bull[0], bull[1], 30, 15)
        if bullRect.colliderect(b):
            bossHealth -= 1
        draw.rect(screen, (0, 255, 0), bullRect)


    # draw.rect(screen, (255, 0, 0), b, 3) #hitbox

    if myTime % 60 == 0: #this is for counting all the time passed
        timePassed.append('t')

    # draw.rect(screen, (255, 0, 0), (b[0], b[1] - 25, b[2] - (5*(30 - bossHealth)), 20)) #health boss
    draw.rect(screen, (255, 0, 0), (b[0], b[1] - 25, 360, 20))
    draw.rect(screen, (25, 25, 25), (b[0], b[1] - 25, 360 - ((360/30)* (30 - bossHealth)), 20))

    myTime += 1
    shortcutFunctions.timeFont(timeFont, timePassed, 500)
    # print(b)
    # print(p.colliderect(b))
    display.set_caption("Super Swordy Boy - FINAL BOSS     FPS = " + str(int(myClock.get_fps())))
    display.update()
    myClock.tick(60)

def moveGuy(p, player, sprites, b, bullets, playerBullets):
    global vPlayer
    global rapid

    keys = key.get_pressed()


    leftEnd = 46
    rightEnd = 978

    if keys[K_SPACE] and p[Y] + p[H] == vPlayer[BOT] and vPlayer[Y] == 0: #fix this area
        vPlayer[Y] = jumpSpeed

    if keys[K_x]:
        player[ROW] = 0

    elif keys[K_LEFT] and p[X] > leftEnd and Rect(p[X] -5, p[Y], p[W], p[H]).colliderect(b) == 0:
        shortcutFunctions.moveGuyLeftBoss(p, player, vPlayer, leftEnd, rightEnd)

    elif keys[K_RIGHT] and p[X] < rightEnd and Rect(p[X] + 5, p[Y], p[W], p[H]).colliderect(b) == 0:
        shortcutFunctions.moveGuyRightBoss(p, player, vPlayer, leftEnd, rightEnd)

    else:
        player[COL] = 0
        player[COL] -= 0.2
        vPlayer[X] = 0

    player[COL] += 0.2

    if player[COL] >= len(sprites[ROW]):
        player[COL] = 1

    p[X] += vPlayer[X]
    player[X] = p[X]
    vPlayer[Y] += gravity

    movePlayerBullets(p, playerBullets)

    # shortcutFunctions.playerBullets(bullets, rapid, p, 5)

def movePlayerBullets(p, bullets):
    for bull in bullets:
        bull[0] += bull[2]
        bull[1] += bull[3]
        if bull[0] > 978:
            bullets.remove(bull)


def moveBoss(boss, b, timePassed, p, bossSprites):
    global vBoss
    global gravity

    # if 5 < len(timePassed) < 10:
    # if len(timePassed) > 12:
    #     vBoss[X] = 0
    #     for i in range(2):
    #         if b[X] < 600:
    #             vBoss[X] = 12

    # elif len(timePassed) > 10:
    #     vBoss[Y] = jumpSpeed

    # elif len(timePassed) > 5:
    #     shortcutFunctions.moveBossBetween(boss, b, vBoss, timePassed)




    # elif len(timePassed) > 12:
    #     vBoss[X] = 0
    #     for i in range(2):
    #         if b[X] < 600:
    #             vBoss[X] = 12
    # if 11 < len(timePassed) < 16:
    #     shortcutFunctions.moveBossPhaseTwo(boss, b, vBoss, p)



    b[X] += vBoss[3]
    if b[X] > 620 or b[X] < 300:
        vBoss[3] = -vBoss[3]
        vBoss[Y] = -30

    b[X] += vBoss[X]
    vBoss[Y] += gravity

    if len(timePassed) % 5 == 0 and len(timePassed) > 0:
        boss[ROW] = 2
    elif vBoss[3] < 0:
        boss[ROW] = 4
    elif vBoss[3] > 0:
        boss[ROW] = 3
    else:
        boss[COL] = 0
        boss[COL] -= 0.2

    boss[COL] += 0.05

    if boss[COL] >= len(bossSprites[ROW]):
        boss[COL] = 0


    # screen.fill((0))

def checkCollision(p, player, sprites, boss, b, bullets):
    keys = key.get_pressed()

    global vPlayer
    global bullSpeed
    global rapid
    global timePassed
    global vBoss
    global bossHealth
    global playerBullets

    if rapid < 20:
        rapid += 1

    shortcutFunctions.playerSprites(player, p, sprites, vPlayer, p[X])
    hitBox = shortcutFunctions.playerSprites(player, p, sprites, vPlayer, p[X])

    p[Y] += vPlayer[Y]
    player[Y] += vPlayer[Y]

    p[H] = hitBox[H]
    p[W] = hitBox[W]

    b[Y] += vBoss[Y]

    if len(timePassed) % 5 == 0 and len(timePassed) > 0:
        shortcutFunctions.createBossBullets(bullets, bullSpeed, b, rapid)
    

    if rapid < 50:
        rapid += 1

    if keys[K_z] and rapid == 50:
        playerBullets.append([p[X], p[Y], 5, 0])
        rapid = 0

    # checkBullBossHits(playerBullets, b, bossHealth)

    

    
    # shortcutFunctions.playerBullets(bullets, rapid, p, 5, timePassed)

    

    # elif 15 < len(timePassed) < 20:
    #     shortcutFunctions.moveBossBetween(boss, b, vBoss)
    
    # elif len(timePassed) == 20:
    #     shortcutFunctions.moveBossPhaseTwo(boss, b, vBoss, player, p)

    # elif len(timePassed) == 25:
    #     shortcutFunctions.createBossBulletsPhase2(bullets, rapid, b)
    #     shortcutFunctions.checkBossBullets(bullets)

    shortcutFunctions.checkBossBullets(bullets)
    checkBullBossHits(playerBullets, b, bossHealth)
    # shortcutFunctions.checkPlayerBullets(bullets)

    if p[X] > 978 and keys[K_RIGHT]:
        p[X] = 978 - hitBox[W]
        vPlayer[X] = 0
        if vPlayer[X] > 0:
            vPlayer[X] = 0

    if player[ROW] == 0 and player[COL] == 3 and p.colliderect(b) and bossHealth > 0:
        bossHealth -= 1
    else:
        visible = False

    print(bossHealth)



    if p[Y] + hitBox[H] >= GROUND:
        vPlayer[BOT] = GROUND
        p[Y] = GROUND - hitBox[H]
        vPlayer[Y] = 0

    if boss[Y] + b[H] >= GROUND:
        vBoss[BOT] = GROUND
        boss[Y] = b[Y] = GROUND - b[H]
        vBoss[Y] = 0

    # if b[Y] + b[H] >= GROUND:
    #     vBoss[BOT] = GROUND
    #     b[Y] = GROUND - b[H]
    #     vBoss[Y] = 0

def checkBullBossHits(bull, boss, health):
    for b in bull:
        bRect = Rect(b[0], b[1], 30, 15)
        if bRect.colliderect(boss):
            bull.remove(b)
            health -= 1
            break