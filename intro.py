'''
intro.py
ICS3U FSE
'''
from pygame import *

screen = display.set_mode((1024, 768))

X = 0
Y = 1
ROW = 2
COL = 3



def draw_introScene(player, picList, mB, mW):
    'This function draws the scene'
    screen.fill((0))

    col = int(player[COL]) #getting the col number for pic

    pic = picList[4][col]

    if player[X] == 683:
        screen.blit(background, (mB, 0))
        screen.blit(walking, (mW, 0))

        screen.blit(pic, (player[X], player[Y])) #blitting the correct position

    else:
        screen.blit(pic, (player[X], player[Y])) #blitting the correct position
    
    display.flip()


def move_intro(player, picList, mB, mW):
    'This function moves the player'
    player[ROW] = 0

    if player[X] < 683:
        player[X] += 7

    else:
        player[X] = 683
        mB -= 300
        mW -= 3072

    player[COL]=player[COL]+0.2 #advancing to the "next" frame

    if player[COL]>=len(picList[ROW]):
        player[COL] = 1   

# def newBackground(player):
#     if player[X] == 683:
#         screen.blit(background, (moveBackground, 0))
#         moveBackground += 1
#         screen.blit(walking, (moveWalking, 0))
#         moveWalking += 3

walking = image.load("Backgrounds/ToWalk1.png")
background = image.load("Backgrounds/Back1.png")
