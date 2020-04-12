'''
intro.py
ICS3U FSE
'''

def draw_intro(screen, player, picList):
    screen.fill(BLACK)
    screen.blit(picList[4][int(frame)], (0, 500))
    frame += 0.3
    if frame == 12:
        frame = 0


def move_player(player):
    player[0] += 1
    
    
