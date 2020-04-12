'''
fade.py

This program is for creating cross dissolve transitions
'''
from pygame import *

def crossDissolveIn():
    for i in range(255):
       screen.set_alpha(i)
