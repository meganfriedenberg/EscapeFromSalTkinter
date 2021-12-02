# Megan Friedenberg
# ITP 499, 10:00-10:50a.m.
# Escape from SAL 2D game


import random
from tkinter import *

class EscapeSalGame:
    def __init__(self):
        # add more variables as needed
        self.width = 600
        self.height = 450
        self.frameRate = 60 # cannot move faster than 60fps
        self.mode = "splashScreen"
        self.playerImg = "player.png" # can't create photoImage here because init it called before Tk()
        self.playerX = 40
        self.playerY = 40
        self.keyX = 40
        self.keyY = 250
        self.doorOpen = False
        self.playerHealth = 0
        self.score = 0
        self.currHighScore = 0
        self.updateSkeletons = {}
        self.updateCouches = {}
        self.playerItems = [] # items we are currently holding
        self.worldItems = ["candy", "key", "heart"]
        self.timeLeft = 15.0  # change later
        self.skeletonPositions = {}   #  will hold data as "skeletonName" : [pos x, pos y]