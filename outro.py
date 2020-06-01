#outro.py
from pygame import *

screen = display.set_mode((1024, 768))
myClock = time.Clock()

backPic1 = image.load('Backgrounds/OutroBackground1.png').convert()
backPic2 = image.load('Backgrounds/OutroBackground2.png').convert()
logo = image.load('Intro Pictures/Logo.png')

player = [512, 625, 4, 0]
pRect = Rect(512, 625, 50, 50)

X = 0
Y = 1
W = 2
H = 3
ROW = 2
COL = 3
BOT = 2

b1 = [0, 0, 1024]; b2 = [1024, 0, 1024]; speed = 7

myCounter = 0
timePassed = []

thank = image.load('Backgrounds/ThankYou.png')

def drawScene(player, p, picList, timePassed, myCounter):
    col = int(player[COL]) #getting the col number for pic
    pic = picList[4][col]

    screen.blit(backPic1, (b1[X], b1[Y]))
    screen.blit(backPic2, (b2[X], b2[Y]))

    b1[X] -= speed
    if abs(b1[X] - speed) > abs(b1[W]):
        b1[X] = b2[W]

    b2[X] -= speed
    if abs(b2[X] - speed) > abs(b2[W]):
        b2[X] = b1[W]

    screen.blit(pic, (player[X], player[Y])) #blitting the correct position

    player[COL] += 0.2
    if player[COL] >= len(picList[ROW]):
        player[COL] = 1

    if 100 < len(timePassed) < 1500:
        screen.blit(thank, (0, 0))


    # print(timePassed)
        

    

    if myCounter % 60 == 0:
        timePassed.append('t')

    # if len(timePassed) >= 200:
    #     fade(1024, 768)

    myCounter += 1


    display.update()
    myClock.tick(60)


def fade(width, height): 
    fade = Surface((width, height))
    fade.fill((0,0,0))
    for alpha in range(0, 300):
        fade.set_alpha(alpha)
        screen.blit(fade, (0,0))
        display.update()
        # time.delay(5)