#outro.py
from pygame import *

screen = display.set_mode((1024, 768))
myClock = time.Clock()

#backgrounds for infinite scrolling
backPic1 = image.load('Backgrounds/OutroBackground1.png').convert()
backPic2 = image.load('Backgrounds/OutroBackground2.png').convert()
# logo = image.load('Intro Pictures/Logo.png')

#player objects
player = [512, 625, 4, 0]
pRect = Rect(512, 625, 50, 50)

#list navigation
X = 0
Y = 1
W = 2
H = 3
ROW = 2
COL = 3
BOT = 2

#pos for backgrounds
b1 = [0, 0, 1024]; b2 = [1024, 0, 1024]; speed = 7

#time
myCounter = 0
timePassed = []

thank = image.load('Backgrounds/ThankYou.png')

def drawScene(player, p, picList, timePassed, myCounter):
    col = int(player[COL]) #getting the col number for pic
    pic = picList[4][col]

    screen.blit(backPic1, (b1[X], b1[Y])) #blitting backgrounds
    screen.blit(backPic2, (b2[X], b2[Y]))

    b1[X] -= speed #subtracting pos of b1[x] to speed, moving the background back
    if abs(b1[X] - speed) > abs(b1[W]): #checking if absolute value of b1[X] is greater than width
        b1[X] = b2[W] #goes to b2

    b2[X] -= speed #same as above with b2
    if abs(b2[X] - speed) > abs(b2[W]): #same as above w b2
        b2[X] = b1[W]

    screen.blit(pic, (player[X], player[Y])) #blitting the correct position

    player[COL] += 0.2 #sprite frame
    if player[COL] >= len(picList[ROW]): #see prevoius files for comments
        player[COL] = 1

    if 100 < len(timePassed) < 1500: #checking if its the right time to display thank you message
        #100 and 1500 because the time passed list is adding at a weird rate
        screen.blit(thank, (0, 0))


    # print(timePassed)
        

    

    if myCounter % 60 == 0: #for time, appending to list
        timePassed.append('t')

    # if len(timePassed) >= 200:
    #     fade(1024, 768)

    myCounter += 1 #for time


    display.update()
    myClock.tick(60)