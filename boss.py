#boss.py

from pygame import *
import shortcutFunctions

init()

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
rapid = 20

#player bullets
playerBullets = []

#time
myTime = 0
timePassed = []
timeShown = []
direction = -1

#health
bossHealth = 50
playerHealth = 2
bh=False
visible = True

#door
door = Rect(400, 300, 300, 422)
doorImg = image.load('Other/outroDoor.png')
#other
livesPic = image.load('Other/live.png')

jumpSound = mixer.Sound('audio/effects/Jump.wav')
playerDamage = mixer.Sound('audio/effects/Explosion.wav')
movement = mixer.Sound('audio/effects/movement.wav')
movement.set_volume(.05)
sword = mixer.Sound('audio/effects/sword.wav')
bossJump = mixer.Sound('audio/effects/bossJump.wav')
bossLand = mixer.Sound('audio/effects/bossLanding.wav')
bossBullets = mixer.Sound('audio/effects/bossShooting.wav')
playerBulletsSound = mixer.Sound('audio/effects/Laser1.wav')
bossBulletsCollide = mixer.Sound('audio/effects/Explosion2.wav')
bossDead = mixer.Sound('audio/effects/Randomize4.wav')


def healthCheck(health):
    health -= 1
    return health

def drawScene(p, player, sprites, boss, b, bullets, bossSprites, timeFont, bossHealth, healthPic, playerBullets, playerHealth, visible, lives):
    'this function draws the scene'
    global vPlayer
    global myTime
    global timePassed
    global timeShown

    screen.blit(backPic, (0, 0)) #background

    #sprites
    shortcutFunctions.playerSprites(player, p, sprites, vPlayer, p[X])
    hitbox = shortcutFunctions.playerSprites(player, p, sprites, vPlayer, p[X])
    # print(hitbox[Y] + hitbox[H])

    # shortcutFunctions.drawBossBullets(bullets)
    for bull in bullets: #go through the bullets list
        draw.circle(screen, (0, 255, 0), (int(bull[0]),int(bull[1])), 4) #draw the bullet

    for bull in playerBullets: #go through player bullets
        draw.rect(screen, (123, 255, 123), (bull[X], bull[Y], 30, 10)) #draws the player bullets as a rect

    if playerHealth >= 0:
        screen.blit(shortcutFunctions.healthBar(playerHealth, healthPic), (0, 0))

    if visible: #visible is true when ever the boss has not ran out of health
        draw.rect(screen, (255, 0, 0), (b[X], b[Y] - 50, b[W], 20)) #the health bar DAMAGED (behind the shrinking health bar that is grey)
        draw.rect(screen, (25, 25, 25), (b[X], b[Y] - 50, b[W] - ((b[W] // 50)*(50 - bossHealth)), 20)) #this health bar shrinks, reveals the red health bar. This tactic was shown on one of Tech with Tim videos
        shortcutFunctions.playerSprites(boss, b, bossSprites, vBoss, b[X]) #draws the biss sprites

    elif not visible: #if the boss has ran out of health
        # draw.rect(screen, (255, 0, 0), door)
        screen.blit(doorImg, door) #draw the door


    if myTime % 60 == 0: #for counting how much time passed
        timePassed.append('t') #this list is cleared when bullets are shot (makes bullets better and health work properly)
        timeShown.append('t') #the ACTUAL time, shown on the display

    myTime += 1 #my time, whenever this is an interval 60, 1 second has passed

    shortcutFunctions.timeFont(timeFont, timeShown, 500) #blits the time left in corner of screen

    for i in range(lives+1): #draws the lives in the corner
        screen.blit(livesPic, (10 + 50*i, 80)) #blits all the lives below the health, same as other files
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
        jumpSound.play()
        vPlayer[Y] = jumpSpeed

    if keys[K_x]: #attacking
        sword.play()
        player[ROW] = 0

    elif keys[K_LEFT] and p[X] - 5 > leftEnd and not Rect(p[X] -5, p[Y], p[W], p[H]).colliderect(b): #moving right 
        shortcutFunctions.moveGuyLeftBoss(p, player, vPlayer, leftEnd, rightEnd) #move the guy left

    elif keys[K_RIGHT] and p[X] + 5 < rightEnd and not Rect(p[X] + 5, p[Y], p[W], p[H]).colliderect(b): #moving right
        shortcutFunctions.moveGuyRightBoss(p, player, vPlayer, leftEnd, rightEnd) #move the guy right

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

def moveBoss(boss, b, timePassed, p, bossSprites, bossHealth):
    'move the boss'
    global vBoss
    global gravity

    if len(timePassed) % 5 == 0 and len(timePassed) > 0: #checking if boss is shooting bullets
        boss[ROW] = 2 #crazy sprite
    elif vBoss[3] < 0: #check if moving left
        boss[ROW] = 4 #left sprite
    elif vBoss[3] > 0: #check if moving right
        boss[ROW] = 3 #right moving sprite
    else: #anything else would be idle pos
        boss[COL] = 0
        boss[COL] -= 0.05

    if boss[Y] + 5 == vBoss[BOT] and vBoss[Y] != 0:
        bossLand.play()

    boss[COL] += 0.05 #sprite fram increasing

    if boss[COL] >= len(bossSprites[ROW]): #for making sure no errors in sprites
        boss[COL] = 0

    b[X] += vBoss[3] #add x pos to direction at all times
    if b[X] > 620 or b[X] < 300: #checking if boss should change direction and jump
        bossJump.play()
        vBoss[3] = -vBoss[3] #change direction
        vBoss[Y] = -30 #jump

    b[X] += vBoss[X] #add x pos to vel
    vBoss[Y] += gravity #gravity
    # screen.fill((0))

def checkCollision(p, player, sprites, boss, b, bullets, bossHealth, playerBullets, playerHealth, visible):
    'checks for collision and if able to shoot bullets'
    keys = key.get_pressed()

    #this variables will be returned at the end ofnthe function
    ph=playerHealth #ph is the player health
    bh = bossHealth #bh is the player health

    global vPlayer
    global bullSpeed
    global rapid
    global timePassed
    global vBoss
    # global playerHealth
    # global playerHealth

    if rapid < 20: #checking if its time to use player bullets
        rapid += 1

    shortcutFunctions.playerSprites(player, p, sprites, vPlayer, p[X]) #sprites (specifically for hitboxes)
    hitBox = shortcutFunctions.playerSprites(player, p, sprites, vPlayer, p[X])

    p[Y] += vPlayer[Y] #add vert velocity to player
    player[Y] += vPlayer[Y]

    p[H] = hitBox[H] #set the width and height of player (the hitbox)
    p[W] = hitBox[W]

    # b[Y] += vBoss[Y] #add boss vert velocity

    # print("ttt",timePassed)
    # if len(timePassed) % 5 == 0 and len(timePassed) > 0: #checking if its time for the boss to shoot multiple bullets
    #     shortcutFunctions.createBossBullets(bullets, bullSpeed, b, rapid)
    #     timePassed=[]

    if keys[K_z] and rapid == 20: #checking if enough space between bullets is made and if bullet key was pressed
        playerBulletsSound.play()
        playerBullets.append([p[X], p[Y], bullSpeed, 0]) #add bullets to list
        rapid = 0 #set to 0 to create space
            
    for bull in playerBullets[:]: #go through copy of player bullets list
        bull[0] += bull[2] #increase x pos by vel
        bull[1] += bull[3] #this technically isnt needed, but its good to have it. Its changing the y vel by the vertical vel, which is 0
        if bull[0] + 30 >= 978: #checking if the bullets hit the right end
            playerBullets.remove(bull) #remove the bullet from the actual list

    for bull in playerBullets: #go through the player bullets list again (not a copy)
        bullRect = Rect(bull[0], bull[1], 30, 10) #create a rect object for the bullet
        if b.colliderect(bullRect): #checking if the boss collideed with the bullets
            bossBulletsCollide.play()
            bh -= 1 #minus 1 to the boss health
            playerBullets.remove(bull) #remove the bullet from the player bullets list
            # playerBullets =[]

    bullH = False 
    if visible: #checkinf if the boss is visible ()automatically set to be visible
        b[Y] += vBoss[Y] #add boss vert velocity

        # if len(timePassed) % 5 == 0 and len(timePassed) > 0:
        if len(timePassed) % 3 == 0 and len(timePassed) > 0: #checking if its time for the boss to shoot multiple bullets, was % 5 before 
            bossBullets.play()
            shortcutFunctions.createBossBullets(bullets, bullSpeed, b, rapid)
            timePassed=[]

        for bull in bullets[:]: #[:] is a COPY of the bullets list, goes through bullets list
            bull[0] += bull[2] #add x val to speed
            bull[1] += bull[3] #add y-val to speed
            bRect = Rect(bull[0]-4, bull[1]-4, 8, 8)
            # if bull[0] > 1800 or bull[0] < -800 or bull[1] < -500 or bull[1] > 1400: #off screen
            if bull[0] > 978 or bull[0] < 46 or bull[1] < 0 or bull[1] > GROUND: #checking if bull is off boundaries
                bullets.remove(bull) #remove from screen

        # bullH = False
        for bullet in bullets: #go through boss bullets
            bullRect = Rect(bullet[X] - 4, bullet[Y] - 4, 8, 8) #create rect object for bullet
            if p.colliderect(bullRect) and bullH == False: #checking if player collided with bullet
                ph -= 1 #lower player health by 1
                time.delay(100) #freeze frame to indicate health gone down
                bullets = [] #clear the bullets list for health to work properly
                bullH = True 

        



    # if keys[K_x] and p.colliderect(b) and len(timePassed) % 2 == 0:
    #     bossHealth -= 1
    # checkAttack(player, p, boss, bossHealth) #checks if the boss was attacked

    # print(bossHealth)

    

    # elif 15 < len(timePassed) < 20:
    #     shortcutFunctions.moveBossBetween(boss, b, vBoss)
    
    # elif len(timePassed) == 20:
    #     shortcutFunctions.moveBossPhaseTwo(boss, b, vBoss, player, p)

    # elif len(timePassed) == 25:
    #     shortcutFunctions.createBossBulletsPhase2(bullets, rapid, b)
    #     shortcutFunctions.checkBossBullets(bullets)

    # shortcutFunctions.checkBossBullets(bullets, p, playerHealth)


    # for bull in bullets[:]: #[:] is a COPY of the bullets list, goes through bullets list
    #     bull[0] += bull[2] #add x val to speed
    #     bull[1] += bull[3] #add y-val to speed
    #     bRect = Rect(bull[0]-4, bull[1]-4, 8, 8)
    #     if bull[0] > 1800 or bull[0] < -800 or bull[1] < -500 or bull[1] > 1400: #off screen
    #         bullets.remove(bull) #remove from screen

    # print("before",len(bullets))

    # bullH = False
    # for bullet in bullets:
    #     bullRect = Rect(bullet[X] - 4, bullet[Y] - 4, 8, 8)
    #     if p.colliderect(bullRect) and bullH == False:
    #         ph -= 1
    #         time.delay(100)
    #         bullets = []
    #         bullH = True
            # print('hello')

        if player[ROW] == 0 and int(player[COL]) == 4 and p.colliderect(b): #checking if the players attack collides with the boss
            bh -= 0.2 #need a fix here
        
        if player[ROW] != 0 and p.colliderect(b): #checking if player is not attacking and player touches the boss
            ph = -1 #player dies

        if b[Y] + b[H] >= GROUND: #same ground mechanics as player, see other files for comments
            vBoss[BOT] = GROUND
            b[Y] = GROUND - b[H]
            vBoss[Y] = 0

        if bh < 0: #checking if the boss health is less than 0
            bossDead.play()
            visible = False #not visible anymore
            
    if not visible and p.colliderect(b): 
        ph = ph


    #checking if player and boss are on the ground
    if p[Y] + hitBox[H] >= GROUND:
        vPlayer[BOT] = GROUND
        p[Y] = GROUND - hitBox[H]
        vPlayer[Y] = 0

    # if b[Y] + b[H] >= GROUND:
    #     vBoss[BOT] = GROUND
    #     b[Y] = GROUND - b[H]
    #     vBoss[Y] = 0

    print(bh)

    # if bh < 0:
    #     visible = False
   
    return bullets,ph,bullH, playerBullets, int(bh), visible

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

def hitPlayer_Health(health):
    if health > -1:
        health -= 1
    return health


##def hitPlayer(p, bullets, playerHealth): 
##    # global playerHealth
##    bullH = False
##    for bullet in bullets:
##        bullRect = Rect(bullet[X] - 4, bullet[Y] - 4, 8, 8)
##        if p.colliderect(bullRect) and bullH == False:
##            playerHealth -= 1
##            bullH = True
##            print('hello')
##    return playerHealth
            # bullets.remove(bull)
        # else:
        #     playerHealth = playerHealth
        # return health
        # else:
    # return health
            # hitPlayer_Health(health)

def mainHealth(health):
    return health

def underBoss(b, p):
    global playerHealth
    if p[X] + p[W] > b[X] and p[X] < b[X] + b[W] and vBoss[Y] < 0 and p[Y] > boss[Y] + boss[H]:
        health = -1

def checkDoor(p, door, visible):
    if not visible:
        if Rect(p[X] + 5, p[Y], p[W], p[H]).colliderect(door) or Rect(p[X] - 5, p[Y], p[W], p[H]).colliderect(door):
            return True
    return False