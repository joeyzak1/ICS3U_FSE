'''
intro.py
ICS3U FSE
'''
from pygame import *

screen = display.set_mode((1024, 768))

X = 0; Y = 1; ROW = 2; COL = 3

introRects = [Rect(337, 275, 350, 75), Rect(337, 375, 350, 75)]
highlight_rects = [(255, 255, 255), (255, 255, 255)]

option_images = [image.load("Intro Pictures/%s%02d.png" %("intro", i)) for i in range(2)]

logo = image.load("Intro Pictures/logo.png")
logoHeight = int((logo.get_height())*0.33)
logoWidth = int((logo.get_width())*0.33)
logo = transform.scale(logo, (logoWidth, logoHeight))

def draw_introScene(player, picList, mB, mW):
    'This function draws the scene'
    mx, my = mouse.get_pos()
    mb = mouse.get_pressed()

    screen.fill((0))

    col = int(player[COL]) #getting the col number for pic

    pic = picList[4][col]

    if player[X] == 683:
        screen.blit(background, (mB, 0))
        screen.blit(walking, (mW, 0))
        screen.blit(logo, (289, -50))

        screen.blit(pic, (player[X], player[Y])) #blitting the correct position

        for i in range(2):
            draw.rect(screen, highlight_rects[i], introRects[i], 3)
            screen.blit(option_images[i], (337, 275+100*i))

            if introRects[i].collidepoint(mx, my) and mb[0] == 1:
                highlight_rects[i] = (0, 255, 0)

            elif introRects[i].collidepoint(mx, my):
                highlight_rects[i] = (0, 0, 255)

            else:
                highlight_rects[i] = (255, 255, 255)

    else:
        screen.blit(pic, (player[X], player[Y])) #blitting the correct position




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



walking = image.load("Backgrounds/ToWalk1.png")
background = image.load("Backgrounds/Back1.png")
