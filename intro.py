'''
intro.py
ICS3U FSE
'''
from pygame import *

init()


screen = display.set_mode((1024, 768))
helpDialog = False #boolean variable for checking if help screen should be on

X = 0; Y = 1; ROW = 2; COL = 3; W = 2 #list nav

introRects = [Rect(337, 275, 350, 75), Rect(337, 375, 350, 75)] #rects to click on
highlight_rects = [(255, 255, 255), (255, 255, 255)] #colours for highlighting

option_images = [image.load("Intro Pictures/%s%02d.png" %("intro", i)).convert() for i in range(2)] #images that go on the rects

logo = image.load("Intro Pictures/logo.png") #logo
logoHeight = int((logo.get_height())*0.33) #width and height
logoWidth = int((logo.get_width())*0.33)
logo = transform.scale(logo, (logoWidth, logoHeight)) #size of logo

b1 = [0, 0, 1024]; b2 = [1024, 0, 1024]; speed = 7 #for background

myClock = time.Clock()
#time
timePassed = []
timeCounter = 0

selectSound = mixer.Sound('audio/effects/Blip_Select.wav')

def draw_introScene(player, picList, mB, mW):
    'This function draws the scene'
    global helpDialog
    global timePassed
    global timeCounter

    mx, my = mouse.get_pos()
    mb = mouse.get_pressed()

    screen.fill((0))

    col = int(player[COL]) #getting the col number for pic

    pic = picList[4][col]
    t=0

    if player[X] == 683: #checking if the players s coord is 683
        screen.blit(background_imgs[0], (b1[X], b1[Y])) #blitting the backgrounds
        screen.blit(background_imgs[1], (b2[X], b2[Y]))

        b1[X] -= speed #moving background 1 according to speed
        if abs(b1[X] - speed) > abs(b1[W]): #checkingif it is time to change background
            b1[X] = b2[W] #switch

        b2[X] -= speed #same as above
        if abs(b2[X] - speed) > abs(b2[W]):#same as above
            b2[X] = b1[W]


        screen.blit(logo, (289, -50)) #blit the logo

        screen.blit(pic, (player[X], player[Y])) #blitting the correct position

        for i in range(2): #for highlighting and drawing selection rectangles
            draw.rect(screen, highlight_rects[i], introRects[i], 3) #draws the rects for highlighting with the correct colour
            screen.blit(option_images[i], (337, 275+100*i)) #blit the images

            if introRects[i].collidepoint(mx, my) and mb[0] == 1: #checking if any of the rects were clicked on
                highlight_rects[i] = (0, 255, 0) #change highlight colour to green

            elif introRects[i].collidepoint(mx, my): #checking if any of the rects were hovered over
                highlight_rects[i] = (0, 0, 255) #change highlight col to blue

            else: #nothing
                highlight_rects[i] = (255, 255, 255) #white
            

        if mb[0] == 1 and introRects[1].collidepoint(mx, my): #checking if help was clicked
            helpDialog = True #sets help to true (will display help in another function)
            t = len(timePassed)

        help(timePassed, t) #help screen (only activates whehn helpdialog is treu)
        # mixer.music.load('audio/MainMenuMusic.mp3')
        # mixer.music.play(-1)

    else: #if player is not at 683
        print(timeCounter)
        screen.blit(pic, (player[X], player[Y])) #blitting the correct position

    if timeCounter % 60 == 0:
        timePassed.append('t')
    timeCounter += 1
    display.update()
    myClock.tick(60)
    display.set_caption("Super Swordy Boy - Intro Screen     FPS = " + str(int(myClock.get_fps())))




def move_intro(player, picList, mB, mW):
    'This function moves the player'
    player[ROW] = 0 #sprite row is 0

    if player[X] < 683: #checking if less than 683, increase pos if less
        player[X] += 7

    else: #if 683
        player[X] = 683 #sets player at that pos
        mB -= 300 #for move background (remove these)
        mW -= 3072

    player[COL] += 0.2 #advancing to the "next" frame

    if player[COL]>=len(picList[ROW]): #making sure no errors occur with sprites
        player[COL] = 1   

def help(timePassed, t):
    'Help screen'
    global helpDialog #get the boolean variable
    if helpDialog: #checking if help dialog is selected
        screen.blit(helpImg, (0, 0)) #blits the picture
        if len(timePassed) - t == 10: #this is for how long to leave on the screen (timepassed list was being weird)
            helpDialog = False #sops the list


background_imgs = [image.load("Backgrounds/back_" + str(i) + ".png").convert() for i in range(2)] #background images
helpImg = image.load('Intro Pictures/Help.png') #help image