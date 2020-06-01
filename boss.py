#boss.py

from pygame import *
import shortcutFunctions

screen = display.set_mode((1024, 768))
myClock = time.Clock()

backPic = image.load('Backgrounds/bossBack.png').convert() #backgorund

#navigation variables
X = 0
Y = 1
W = 2
H = 3
ROW = 2
COL = 3
BOT = 2
#ground variables for velocity vertical
GROUND = 722
bottom = GROUND

#jumping
jumpSpeed = -20
gravity = 1

#player
player = [150, 650, 4, 0]
pRect = Rect(150, 650, 20, 45)

#boss
boss = [600, 449, 0, 0]
bossRect = Rect(600, 450, 300, 272)

#direction of boss
direction = -1

#velocities
vPlayer = [0, 0, bottom]
vBoss = [0, 0, bottom, direction]

#bullets
bullSpeed = 5
bullets = []
rapid = 50

#player bullets
playerBullets = []

#time
myTime = 0
timePassed = []
direction = -1

#health
bossHealth = 25

def drawScene(p, player, sprites, boss, b, bullets, bossSprites, timeFont, bossHealth, playerBullets):
    'this function draws the scene'
    global vPlayer
    global myTime
    global timePassed

    screen.blit(backPic, (0, 0))

    #sprites
    shortcutFunctions.playerSprites(player, p, sprites, vPlayer, p[X])
    hitbox = shortcutFunctions.playerSprites(player, p, sprites, vPlayer, p[X])
    shortcutFunctions.playerSprites(boss, b, bossSprites, vBoss, b[X])
    # print(hitbox[Y] + hitbox[H])

    # shortcutFunctions.drawBossBullets(bullets)
    for bull in bullets: #go through the bullets list
        draw.circle(screen, (0, 255, 0), (int(bull[0]),int(bull[1])), 4) #draw the bullet

    for bull in playerBullets: #go through player bullets
        draw.rect(screen, (0, 255, 0), (bull[X], bull[Y], 30, 10))
    draw.rect(screen, (255, 0, 0), b, 3) #hitbox

    if myTime % 60 == 0: #for counting how much time passed
        timePassed.append('t')

    myTime += 1 #my time

    shortcutFunctions.timeFont(timeFont, timePassed, 500) #blits the time left in corner of screen
    # print(b)
    # print(p.colliderect(b))
    display.set_caption("Super Swordy Boy - FINAL BOSS     FPS = " + str(int(myClock.get_fps()))) #the title
    display.update()
    myClock.tick(60)

def moveGuy(p, player, sprites, b, bossSprites, timeFont, playerBullets):
    'moves the player'
    global vPlayer
    global rapid

    keys = key.get_pressed()

    #left and right end of display
    leftEnd = 46
    rightEnd = 978

    if keys[K_SPACE] and p[Y] + p[H] == vPlayer[BOT] and vPlayer[Y] == 0: #jump (see other files for comments)
        vPlayer[Y] = jumpSpeed

    if keys[K_x]: #attacking
        player[ROW] = 0

    elif keys[K_LEFT] and p[X] > leftEnd and not Rect(p[X] -5, p[Y], p[W], p[H]).colliderect(b): #moving right 
        shortcutFunctions.moveGuyLeftBoss(p, player, vPlayer, leftEnd, rightEnd)

    elif keys[K_RIGHT] and p[X] < rightEnd and not Rect(p[X] + 5, p[Y], p[W], p[H]).colliderect(b) == 0: #moving right
        shortcutFunctions.moveGuyRightBoss(p, player, vPlayer, leftEnd, rightEnd)

    else: #so sprite is on idle and player doesnt move
        player[COL] = 0
        player[COL] -= 0.2
        vPlayer[X] = 0

    player[COL] += 0.2 #sprite frame increase by 0.2

    if player[COL] >= len(sprites[ROW]): #making sure program doesnt crash
        player[COL] = 1

    p[X] += vPlayer[X] #adding vel to players pos
    player[X] = p[X]
    vPlayer[Y] += gravity

    createPlayerBullets(playerBullets, p, 5, timePassed) #creates players velocity
    movePlayerBullets(playerBullets) #moves the players bullets

def movePlayerBullets(bullets):
    'move the players bullets'
    for bull in bullets[:]: #go through copy of bull list
        bull[0] += bull[2] #add x pos to vel
        bull[1] += bull[3] #add y pos to vel
        if bull[0] > 978: #check if bull is off screen
            bullets.remove(bull)

def moveBoss(boss, b, timePassed, p, bossSprites, bossHealth):
    'move the boss'
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

    if len(timePassed) % 5 == 0 and len(timePassed) > 0: #checking if boss is shooting bullets
        boss[ROW] = 2 #crazy sprite
    elif vBoss[3] < 0: #check if moving left
        boss[ROW] = 4 #left sprite
    elif vBoss[3] > 0: #check if moving right
        boss[ROW] = 3 #right moving sprite
    else: #anything else would be idle pos
        boss[COL] = 0
        boss[COL] -= 0.05

    boss[COL] += 0.05 #sprite fram increasing

    if boss[COL] >= len(bossSprites[ROW]): #for making sure no errors in sprites
        boss[COL] = 0

    b[X] += vBoss[3] #add x pos to direction at all times
    if b[X] > 620 or b[X] < 300: #checking if boss should change direction and jump
        vBoss[3] = -vBoss[3] #change direction
        vBoss[Y] = -30 #jump

    b[X] += vBoss[X] #add x pos to vel
    vBoss[Y] += gravity #gravity
    # screen.fill((0))

def checkCollision(p, player, sprites, boss, b, bullets, bossHealth, playerBullets):
    'checks for collision'
    keys = key.get_pressed()

    global vPlayer
    global bullSpeed
    global rapid
    global timePassed
    global vBoss

    if rapid < 20: #checking if its time to use player bullets
        rapid += 1

    shortcutFunctions.playerSprites(player, p, sprites, vPlayer, p[X]) #sprites (specifically for hitboxes)
    hitBox = shortcutFunctions.playerSprites(player, p, sprites, vPlayer, p[X])

    p[Y] += vPlayer[Y] #add vert velocity to player
    player[Y] += vPlayer[Y]

    p[H] = hitBox[H]
    p[W] = hitBox[W]

    b[Y] += vBoss[Y] #add boss vert velocity

    if len(timePassed) % 5 == 0 and len(timePassed) > 0: #checking if its time for the boss to shoot multiple bullets
        shortcutFunctions.createBossBullets(bullets, bullSpeed, b, rapid)

    # if keys[K_x] and p.colliderect(b) and len(timePassed) % 2 == 0:
    #     bossHealth -= 1
    checkAttack(player, p, boss, bossHealth) #checks if the boss was attacked

    print(bossHealth)

    

    # elif 15 < len(timePassed) < 20:
    #     shortcutFunctions.moveBossBetween(boss, b, vBoss)
    
    # elif len(timePassed) == 20:
    #     shortcutFunctions.moveBossPhaseTwo(boss, b, vBoss, player, p)

    # elif len(timePassed) == 25:
    #     shortcutFunctions.createBossBulletsPhase2(bullets, rapid, b)
    #     shortcutFunctions.checkBossBullets(bullets)

    shortcutFunctions.checkBossBullets(bullets)
    checkBullBossHits(playerBullets, b, bossHealth)

    #checking if player and boss are on the ground
    if p[Y] + hitBox[H] >= GROUND:
        vPlayer[BOT] = GROUND
        p[Y] = GROUND - hitBox[H]
        vPlayer[Y] = 0

    if b[Y] + b[H] >= GROUND:
        vBoss[BOT] = GROUND
        b[Y] = GROUND - b[H]
        vBoss[Y] = 0

def checkAttack(player, p, boss, bossHealth):
    'checking if the player attacked the boss'
    row = player[ROW] #gets the row of the player
    col = int(player[COL]) #gets the col of the player

    if row == 0 and col == 5: #checking if attack sprite will go over
        col = 0

    if row == 0 and col == 4: #checking if correct sprite is on to attack
        if p.colliderect(Rect(boss[X], boss[Y], 300, 272)): #checking if the player is touching the boss
            bossHealth -= 1 #lowers the boss health

def createPlayerBullets(bullets, p, SPEED, timePassed):
    'creating player bullets'
    keys = key.get_pressed()
    if keys[K_z] and len(timePassed) % 5 == 0: #checking if keys were clicked and its time for bullets to be created
        bullets.append([p[X], p[Y], SPEED, 0]) #add bullets

def checkBullBossHits(bull, boss, bossHealth):
    'checks if bullets collide'
    for b in bull: 
        bRect = Rect(b[0], b[1], 30, 15)
        if bRect.colliderect(boss):
            bull.remove(b)
            break