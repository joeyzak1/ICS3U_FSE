'''
intro.py
ICS3U FSE
'''
from pygame import *

def draw_introScene(screen, player, picList, ROW, COL, X, Y):

    screen.fill((0)) 

    col = int(player[COL]) #getting the col number for pic

    pic = picList[4][col]

    screen.blit(pic, (player[X], player[Y])) #blitting the correct position
    display.flip()

def move_intro(player, ROW, X, COL, picList):

    player[ROW] = 0
    player[X] += 7

    player[COL]=player[COL]+0.2 #advancing to the "next" frame

    if player[COL]>=len(picList[ROW]):
        player[COL] = 1   
