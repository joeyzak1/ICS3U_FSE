#boss.py

from pygame import *
import shortcutFunctions

screen = display.set_mode((1024, 768))
myClock = time.Clock()

backPic = image.load('Backgrounds/bossBack.png').convert()

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

player = [150, 650, 4, 0]
pRect = Rect(150, 650, 20, 45)

boss = [600, 450, 0, 0]
bossRect = Rect(600, 450, 300, GROUND-450)

vPlayer = [0, 0, bottom]
vBoss = [0, 0, bottom]

bullSpeed = 5
bullets = []
rapid = 0

myTime = 0
timePassed = []

def drawScene(p, player, sprites, boss, b, bullets):
    global vPlayer
    global myTime
    global timePassed

    screen.blit(backPic, (0, 0))

    shortcutFunctions.playerSprites(player, p, sprites, vPlayer, p[X])
    hitbox = shortcutFunctions.playerSprites(player, p, sprites, vPlayer, p[X])

    shortcutFunctions.drawBossBullets(bullets)
    draw.rect(screen, (255, 0, 0), b)

    if myTime % 60 == 0:
        timePassed.append('t')

    myTime += 1
    print (timePassed)
    display.update()
    myClock.tick(60)

def moveGuy(p, player, sprites):
    global vPlayer
    global rapid

    keys = key.get_pressed()


    leftEnd = 46
    rightEnd = 978

    if keys[K_SPACE] and p[Y] + p[H] == vPlayer[BOT] and vPlayer[Y] == 0: #fix this area
        vPlayer[Y] = jumpSpeed

    if keys[K_x] and rapid == 20:
        player[ROW] = 0

    elif keys[K_LEFT] and p[X] > leftEnd:
        shortcutFunctions.moveGuyLeftBoss(p, player, vPlayer, leftEnd, rightEnd)

    elif keys[K_RIGHT] and p[X] < rightEnd:
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

def moveBoss(b):
    global vBoss

    b[X] += vBoss[X]
    # vBoss[Y] += gravity
    # screen.fill((0))

def checkCollision(p, player, sprites, boss, b, bullets):
    keys = key.get_pressed()

    global vPlayer
    global bullSpeed
    global rapid
    global timePassed
    global vBoss

    if rapid < 20:
        rapid += 1

    shortcutFunctions.playerSprites(player, p, sprites, vPlayer, p[X])
    hitBox = shortcutFunctions.playerSprites(player, p, sprites, vPlayer, p[X])

    p[Y] += vPlayer[Y]
    player[Y] += vPlayer[Y]

    p[H] = hitBox[H]
    p[W] = hitBox[W]

    b[Y] += vBoss[Y]

    if len(timePassed) == 10:
        shortcutFunctions.createBossBullets(bullets, bullSpeed, b, rapid)
        shortcutFunctions.checkBossBullets(bullets)

    elif len(timePassed) == 15:
        shortcutFunctions.moveBossBetween(boss, b, vBoss)
    
    elif len(timePassed) == 20:
        shortcutFunctions.moveBossPhaseTwo(boss, b, vBoss, player, p)


    if p[Y] + hitBox[H] >= GROUND:
        vPlayer[BOT] = GROUND
        p[Y] = GROUND - hitBox[H]
        vPlayer[Y] = 0