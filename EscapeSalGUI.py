# Megan Friedenberg
# ITP 499, 10:00-10:50a.m.
# Escape from SAL 2D game

from tkinter import *
from EscapeSalGame import *



class EscapeSalGUI:
    def __init__(self, initial):
        root = Tk() # initializes Tkinter
        root.title("Escape From SAL GUI")
        root.geometry("550x450")
        self.root = root
        self.myFrame = Frame(root)
        self.mode = initial


    def splashScreenButtonClicked(self):
        self.mode = "Play"

    def helpButtonClicked(self):
        self.mode = "Help"
        top = Toplevel()
        top.mainloop()

    def drawGame(self):
        if self.mode == "splashScreen":
            self.myFrame.grid()
            self.label1 = Label(self.myFrame, text="Escape from SAL!")
            self.label1.config(font="Arial 14 bold", fg="red")
            self.label1.grid(row=5, column=300)
            self.mainButton = Button(self.myFrame, text="Play!", command=self.splashScreenButtonClicked)
            self.helpButton = Button(self.myFrame, text="Help", command=self.helpButtonClicked)
            self.helpButton.grid(row=500, column=500)
            self.mainButton.grid(row=2, column=0)
        if self.mode == "Play":
            self.root.configure(bg="blue")

    def run(self):
       self.drawGame()

## CMU's mode dispatcher ##
def redrawScreen(canvas, gameData):
    if gameData.mode == "splashScreen":
        splashScreenRedrawScreen(canvas, gameData)
    elif gameData.mode == "play":
        playScreenRedrawScreen(canvas, gameData)
    elif gameData.mode == "help":
        return
    elif gameData.mode == "gameOver":
        return
    elif gameData.mode == "win":
        winScreenRedrawScreen(canvas, gameData)
    elif gameData.mode == "gameOver":
        gameOverScreenRedrawScreen(canvas, gameData)

def mouseClicked(event, gameData):
    if(gameData.mode == "splashScreen"):
        splashScreenMouseClicked(event, gameData)
    elif gameData.mode == "play":
        return
    elif gameData.mode == "help":
        helpScreenMouseClicked(event, gameData)
    elif gameData.mode == "win":
        winScreenMouseClicked(event, gameData)
    elif gameData.mode == "gameOver":
        gameOverScreenMouseClicked(event, gameData)

def keyPressed(event, gameData):
    if gameData.mode == "splashScreen":
        splashScreenKeyPressed(event, gameData)
    elif gameData.mode == "help":
        return
    elif gameData.mode == "play":
        playScreenKeyPressed(event, gameData)
    elif gameData.mode == "win":
        return
    elif gameData.mode == "gameOver":
        return


def redrawScreen(canvas, gameData):
    if gameData.mode == "splashScreen":
        splashScreenRedrawScreen(canvas, gameData)
    elif gameData.mode == "help":
        helpScreenRedrawScreen(canvas, gameData)
    elif gameData.mode == "play":
        playScreenRedrawScreen(canvas, gameData)
    elif gameData.mode == "win":
        winScreenRedrawScreen(canvas, gameData)
    elif gameData.mode == "gameOver":
        gameOverScreenRedrawScreen(canvas, gameData)



def updateGame(canvas, gameData):
    if gameData.mode == "splashScreen":
        splashScreenUpdateGame(gameData)
    elif gameData.mode == "help":
        return
    elif gameData.mode == "play":
        playScreenUpdateGame(gameData)
    elif gameData.mode == "win":
        # winScreenUpdateGame(gameData) # this function only gets called once, right when the player wins
        return
    elif gameData.mode == "gameOver":
        gameOverUpdateGame(gameData)


## end dispatcher ##


## play screen functions ##


def playScreenUpdateGame(gameData):
    gameData.timeLeft -= 0.06 # 60 frames fps
    if gameData.timeLeft < 0:
        gameData.mode = "gameOver"
        gameData.score = 0 # if you die, your score is zero
        # gameOverUpdateGame(gameData) # make sure the current high score is grabbed before we die

    # updating skeleton's positions
    # dictionary order is: [posX, posY, directionToMove, minDirection, maxDirection, currentDirection]
    for s in gameData.skeletonPositions:
        roundedNum = round(gameData.timeLeft)
        if roundedNum % 2 == 0: # update moving only every half a sec so enemies don't move toooo fast
            currInfoList = gameData.skeletonPositions[s]
            movingDirection = (currInfoList[2])
            minVal = int(currInfoList[3])
            maxVal = int(currInfoList[4])
            currDir = int(currInfoList[5])
            currX = int(currInfoList[0])
            currY = int(currInfoList[1])
            if movingDirection == "y":
                currY += 10 * currDir
                # print(currY, " ", maxVal)
                if currY < minVal or currY >= maxVal:
                    currDir *= -1
            elif movingDirection == "x":
                currX += (10 * currDir)
                if currX < minVal or currX >= maxVal:
                    currDir *= -1
            gameData.skeletonPositions[s] = [str(currX), str(currY), movingDirection, str(minVal), str(maxVal), str(currDir), True] # reinsert after changing




def playScreenRedrawScreen(canvas, gameData):
    # spawn the player, these vals are saved in our EscapeSalGame()
    canvas.create_rectangle(0, 0, gameData.width, gameData.height, fill='#6699cc',
                             width=0)
    imagePlayer = PhotoImage(file="player.png")
    canvas.playerImg = imagePlayer # gets garbage collected if this line is not present
    canvas.create_image(gameData.playerX, gameData.playerY, image=imagePlayer)

    # print(gameData.skeletonPositions)
    for s in gameData.skeletonPositions:
        roundedNum = round(gameData.timeLeft)
        # print(s)
        if roundedNum % 2 == 0:
            skeletonImage = PhotoImage(file="Skeleton0.png")
            listS = gameData.skeletonPositions[s]
            canvas.skelImg = skeletonImage
            gameData.updateSkeletons[s] = skeletonImage
            canvas.create_image(int(listS[0]), int(listS[1]), image=skeletonImage)
        else:
            listS = gameData.skeletonPositions[s]
            skeletonImage = PhotoImage(file="Skeleton1.png")
            canvas.skelImg = skeletonImage
            gameData.updateSkeletons[s] = skeletonImage
            canvas.create_image(int(listS[0]), int(listS[1]), image=skeletonImage)

    playScreenPositionsFile(canvas, gameData)

    canvas.create_rectangle(gameData.width*7 / 8 - gameData.width / 5, (gameData.height * 6) / 7 - gameData.height / 10,
                            gameData.width*7 / 8 + gameData.width / 12, (gameData.height * 7) / 8 + gameData.height / 80,
                            fill="tan")
    canvas.create_text(gameData.width*3 / 4 - gameData.height / 50, gameData.height*3 / 4 + gameData.height / 15,
                       text="Timer:", font="Arial 12 bold", fill="black")
    time = gameData.timeLeft
    canvas.create_text(gameData.width*3 / 4 + gameData.height / 10, gameData.height*3 / 4 + gameData.height / 15,
                       text="{:.2f}".format(time), font="Arial 12 bold", fill="black")


def checkPlayerEnemyIntersection(gameData):
    for s in gameData.skeletonPositions:
        currList = gameData.skeletonPositions[s]
        skeleX = int(currList[0])
        skeleY = int(currList[1])
        xDiff = abs(skeleX - gameData.playerX)
        yDiff = abs(skeleY - gameData.playerY)
        if xDiff <= 40 and yDiff <= 40:
            if gameData.playerHealth == 0:
                gameData.mode = "gameOver"
                gameData.score = 0  # if you die, your score is zero
            else:
                gameData.playerHealth -= 1

def checkCouchIntersection(gameData):
    if gameData.playerX >= 260 and gameData.playerX <= 330 and gameData.playerY >= 30 and gameData.playerY <= 70:
        return True
    if gameData.playerX >= 260 and gameData.playerX <= 330 and gameData.playerY >= 190 and gameData.playerY <= 260:
        return True

    return False



def playScreenKeyPressed(event, gameData):
    # moving the player
    checkPlayerEnemyIntersection(gameData)
    if event.char == 'w':
        if gameData.playerY < 50:
            gameData.playerY = 50
        else:
            if checkCouchIntersection(gameData) is False:
                gameData.playerY -= 10
                if checkCouchIntersection(gameData) is True:
                    gameData.playerY += 10
            print(gameData.playerX, " ", gameData.playerY)
    elif event.char == 'd':
        if gameData.playerX > 540:
            gameData.playerX = 540
        else:
            if checkCouchIntersection(gameData) is False:
                gameData.playerX += 10
                if checkCouchIntersection(gameData) is True:
                    gameData.playerX -= 10
    elif event.char == 'a':
        if gameData.playerX < 20:
            gameData.playerX = 20
        else:
            if checkCouchIntersection(gameData) is False:
                gameData.playerX -= 10
                if checkCouchIntersection(gameData) is True:
                    gameData.playerX += 10
    elif event.char == 's':
        if gameData.playerY >= 400:
            gameData.playerY = 400
        else:
            if checkCouchIntersection(gameData) is False:
                gameData.playerY += 10
                if checkCouchIntersection(gameData) is True:
                    gameData.playerY -= 10
    elif event.char == 'p':
        if gameData.playerX >= 430 and gameData.playerX <= 470 and gameData.playerY <= 180 and gameData.playerY >= 120:
            if gameData.worldItems.count("key") > 0:  # if we have not already picked up the world's key
                gameData.playerItems.append("key")
                gameData.score += 10
                gameData.worldItems.remove("key")
        if gameData.playerX >= 20 and gameData.playerX <= 30 and gameData.playerY >= 270 and gameData.playerY <= 290:
            if gameData.worldItems.count("heart") > 0:
                gameData.playerItems.append("heart")
                gameData.score += 30
                gameData.playerHealth += 3
                gameData.worldItems.remove("heart")
        if gameData.playerX >= 270 and gameData.playerX <= 330 and gameData.playerY >= 340 and gameData.playerY <= 400:
            if gameData.doorOpen is False:
                if gameData.playerItems.count("key") > 0:
                    gameData.doorOpen = True
            else:
                # the door is already open and we should now "walk" through
                gameData.mode = "win"
                gameData.score += gameData.timeLeft
                winScreenUpdateGame(gameData)



def playScreenPositionsFile(canvas, gameData): # called to help draw the playScreen from textfile
    inputFile = open("worldItems.txt", "r")
    for line in inputFile:
        currList = line.split(",")
        if currList[0] != "stop":
            # then we have more items to create
            if currList[0] == "key" and gameData.playerItems.count("key") == 0:
                imageKey = PhotoImage(file="Key.png")
                canvas.keyImg = imageKey
                canvas.create_image(int(currList[1]), int(currList[2]), image=imageKey)
            if currList[0] == "door":
                if gameData.doorOpen is False:
                    imageDoorClosed = PhotoImage(file="closedDoor-resized2.png")
                    canvas.doorCloseImg = imageDoorClosed
                    canvas.create_image(int(currList[1]), int(currList[2]), image=imageDoorClosed)
                else:  # the door should be opened
                    imageDoorOpen = PhotoImage(file="openDoor-resized.png")
                    canvas.doorOpenImg = imageDoorOpen
                    canvas.create_image(int(currList[1]),int(currList[2]), image=imageDoorOpen)
            if currList[0] == "couch":
                imageCouch = PhotoImage(file="couch.png")
                canvas.couchImg = imageCouch
                couchID = currList[1]
                gameData.updateCouches[couchID] = imageCouch
                canvas.create_image(int(currList[2]), int(currList[3]), image=imageCouch)
            if currList[0] == "heart" and gameData.playerItems.count("heart") == 0:
                imageHeart = PhotoImage(file="heart4.png")
                canvas.heartImg = imageHeart
                canvas.create_image(int(currList[1]), int(currList[2]), image=imageHeart)
            if currList[0] == "skeleton":
                posX = currList[2]
                posY = currList[3]
                #  gameData.skeleX1 = posX
                # gameData.skeleY1 = int(posY)
                skelName = currList[1]
                if skelName not in gameData.skeletonPositions.keys():
                    directionToMove = currList[4]
                    minDirection = currList[5]
                    maxDirection = currList[6]
                    currentDirection = currList[7]
                    gameData.skeletonPositions[skelName] = [posX, posY, directionToMove, minDirection, maxDirection, currentDirection, False]
                # print(gameData.skeletonPositions)



## help screen functions ##

def helpScreenUpdateGame(gameData):
    return  # do nothing, no need for deltaTime

def helpScreenRedrawScreen(canvas, gameData):
    # title
    canvas.create_text(gameData.width / 2 - gameData.height / 15, gameData.height / 2 - gameData.height / 3,
                       text="You are trapped in SAL!", font="Arial 30 bold", fill="black")
    # instructions
    canvas.create_text((gameData.width/2) - gameData.height / 25, (gameData.width/2) - gameData.height / 3,
                       text="Avoid CPs! Grab the key and make it to the exit in time!\n\tOr else YOU become a CP!",
                       font="Arial 12", fill='black')
    canvas.create_text((gameData.width*2 / 3) - gameData.height / 3.8, (gameData.width*2 / 3) - gameData.height / 2.5,
                       text="Use WASD to move, and the spacebar to pick up items and fight CPs!", font="Arial 11", fill='black')

    # button back to the splashScreen
    canvas.create_rectangle(gameData.width / 2 - gameData.width / 5, (gameData.height * 3) / 4 - gameData.height / 8,
                            gameData.width / 2 + gameData.width / 12, (gameData.height * 5) / 6 - gameData.height / 100,
                            fill="yellow")
    canvas.create_text(gameData.width / 2 - gameData.width / 16, (gameData.height * 3) / 4 - gameData.height / 30,
                       text="Back to Main Menu", font="Arial 14")


def helpScreenMouseClicked(event, gameData):
    # bound check if we want to go back to the main menu
    if event.x > (gameData.width / 2) - gameData.width / 5 and event.x < gameData.width / 2 + gameData.width / 12 and \
            event.y > (gameData.height * 3) / 4 - gameData.height / 8 and event.y < (gameData.height * 5) / 6 - gameData.height / 100:
        gameData.mode = "splashScreen"



## starting screen functions ##

def splashScreenUpdateGame(gameData):
    return # do nothing, no need for deltaTime


def splashScreenMouseClicked(event, gameData):
    # need to check if we clicked in the bounds of the help button or the start button

    # bound check for start
    if event.x > gameData.width/2 - gameData.width/5 and event.x < gameData.width/2 + gameData.width/12 and \
            event.y > gameData.height/2 - gameData.height/6 and event.y < gameData.height/2 + gameData.height/15:
        gameData.mode = "play"

    # bound check for help
    if event.x > gameData.width / 2 - gameData.width / 5 and event.x < gameData.width/2 + gameData.width/12 and \
            event.y > (gameData.height*3) / 4 - gameData.height / 8 and event.y < (gameData.height*5) / 6 - gameData.height / 100:
        gameData.mode = "help"



def splashScreenKeyPressed(event, gameData):
    return # you can only click on the homescreen


def splashScreenRedrawScreen(canvas, gameData):
    # title
    canvas.create_text(gameData.width/2 - gameData.height/15, gameData.height/2 - gameData.height/3, text="Escape From SAL!", font="Arial 30 bold", fill="black")

    # start button
    canvas.create_rectangle(gameData.width/2 - gameData.width/5, gameData.height/2 - gameData.height/6,
                gameData.width/2 + gameData.width/12, gameData.height/2 + gameData.height/30, fill="red")
    canvas.create_text(gameData.width/2 - gameData.width/16, gameData.height/2 - gameData.height/15, text="Start", font="Arial 20")

    # help button
    canvas.create_rectangle(gameData.width / 2 - gameData.width / 5, (gameData.height*3) / 4 - gameData.height / 8,
                            gameData.width / 2 + gameData.width / 12, (gameData.height*5) / 6 - gameData.height / 100,
                            fill="yellow")
    canvas.create_text(gameData.width / 2 - gameData.width / 16, (gameData.height*3) / 4 - gameData.height / 30,
                       text="Help", font="Arial 20")


def gameReset(gameData):
    gameData.playerX = 40
    gameData.playerY = 40
    gameData.doorOpen = False
    gameData.playerHealth = 3
    gameData.score = 0
    gameData.currHighScore = 0
    gameData.playerItems = []  # items we are currently holding
    gameData.worldItems = ["candy", "key", "heart"]
    gameData.timeLeft = 15.0  # change later
    gameData.mode = "splashScreen"


## win screen functions ##

def winScreenUpdateGame(gameData):
    # this function is ONLY called right when the player wins
    # it serves to update the highscore if need be on the text file
    inputFile = open("highscore.txt", "r")
    currList = []
    for line in inputFile:
        currList = line.split(",")
    highScore = int(currList[0])
    inputFile.close()

    if gameData.score > highScore: # our score is greater, rewrite and save
        outputFile = open("highscore.txt", 'w').close()  # erases the file contents
        outputFile = open("highscore.txt", 'w')  # so now reopen it
        print(gameData.score, file=outputFile) # write the new highscore
        outputFile.close()
        gameData.currHighScore = gameData.score
    else:
        gameData.currHighScore = highScore # didn't beat the old high score, save it for win/lose screen purposes


def winScreenRedrawScreen(canvas, gameData):
    # title
    canvas.create_text(gameData.width / 2 - gameData.height / 15, gameData.height / 2 - gameData.height / 3,
                       text="You Win!", font="Arial 30 bold", fill="black")
    # instructions
    canvas.create_text((gameData.width / 3) - (gameData.height / 5) + 17, (gameData.width / 2) - gameData.height / 3,
                       text="\tYour score:",
                       font="Arial 12", fill='black')
    time = gameData.score
    currScore = "{:.2f}".format(time)
    canvas.create_text((gameData.width*2 / 3) - gameData.height / 25, (gameData.width / 2) - gameData.height / 3,
                       text=currScore,
                       font="Arial 12", fill='black')
    canvas.create_text((gameData.width / 2) - gameData.height / 3, (gameData.width*2 / 3) - gameData.height / 2.5,
                       text="\tCurrent high score:",
                       font="Arial 12", fill='black')
    roundedHigh = gameData.currHighScore
    currScore = "{:.2f}".format(roundedHigh)
    canvas.create_text((gameData.width*2 / 3) - gameData.height / 25, (gameData.width*2 / 3) - gameData.height / 2.5,
                       text=currScore,
                       font="Arial 12", fill='black')
    # button back to the splashScreen
    canvas.create_rectangle(gameData.width / 2 - gameData.width / 5, (gameData.height * 3) / 4 - gameData.height / 8,
                            gameData.width / 2 + gameData.width / 12, (gameData.height * 5) / 6 - gameData.height / 100,
                            fill="red")
    canvas.create_text(gameData.width / 2 - gameData.width / 16, (gameData.height * 3) / 4 - gameData.height / 30,
                       text="Back to Main Menu", font="Arial 14")



def winScreenMouseClicked(event, gameData):
    # bound check if we want to go back to the main menu
    if event.x > (gameData.width / 2) - gameData.width / 5 and event.x < gameData.width / 2 + gameData.width / 12 and \
            event.y > (gameData.height * 3) / 4 - gameData.height / 8 and event.y < (gameData.height * 5) / 6 - gameData.height / 100:
        gameData.mode = "splashScreen"
        gameReset(gameData)



## begin gameOver functions ##

def gameOverScreenRedrawScreen(canvas, gameData):
    # title
    canvas.create_text(gameData.width / 2 - gameData.height / 15, gameData.height / 2 - gameData.height / 3,
                       text="You Lost!", font="Arial 30 bold", fill="black")
    # instructions
    canvas.create_text((gameData.width / 3) - (gameData.height / 5) + 17, (gameData.width / 2) - gameData.height / 3,
                       text="\tYour score:",
                       font="Arial 12", fill='black')
    canvas.create_text((gameData.width * 2 / 3) - gameData.height / 25, (gameData.width / 2) - gameData.height / 3,
                       text=str(gameData.score),
                       font="Arial 12", fill='black')
    canvas.create_text((gameData.width / 2) - gameData.height / 3, (gameData.width * 2 / 3) - gameData.height / 2.5,
                       text="\tCurrent high score:",
                       font="Arial 12", fill='black')
    roundedHigh = gameData.currHighScore
    currScore = "{:.2f}".format(roundedHigh)
    canvas.create_text((gameData.width * 2 / 3) - gameData.height / 25,
                       (gameData.width * 2 / 3) - gameData.height / 2.5,
                       text=currScore,
                       font="Arial 12", fill='black')
    # button back to the splashScreen
    canvas.create_rectangle(gameData.width / 2 - gameData.width / 5, (gameData.height * 3) / 4 - gameData.height / 8,
                            gameData.width / 2 + gameData.width / 12, (gameData.height * 5) / 6 - gameData.height / 100,
                            fill="blue")
    canvas.create_text(gameData.width / 2 - gameData.width / 16, (gameData.height * 3) / 4 - gameData.height / 30,
                       text="Back to Main Menu", font="Arial 14")


def gameOverScreenMouseClicked(event, gameData):
    # bound check if we want to go back to the main menu
    if event.x > (gameData.width / 2) - gameData.width / 5 and event.x < gameData.width / 2 + gameData.width / 12 and \
            event.y > (gameData.height * 3) / 4 - gameData.height / 8 and event.y < (gameData.height * 5) / 6 - gameData.height / 100:
        gameData.mode = "splashScreen"
        gameReset(gameData)


def gameOverUpdateGame(gameData):
    inputFile = open("highscore.txt", "r")
    currList = []
    for line in inputFile:
        currList = line.split(",")
    gameData.currHighScore = int(currList[0])
    inputFile.close()

## end mode types ##

def run(): # use of wrappers to decide later what to do specifically based on our mode
    def redrawScreenWrapper(canvas, gameData):
        canvas.delete(ALL) # clear the screen
        canvas.create_rectangle(0,0, gameData.width, gameData.height, fill='white', width=0)
        redrawScreen(canvas, gameData)
        canvas.update()

    def mouseClickedWrapper(event,canvas,gameData):
        mouseClicked(event,gameData)
        redrawScreenWrapper(canvas, gameData) # redraw the screen because a button click ALWAYS changes screen


    def keyPressedWrapper(event,canvas, gameData):
        keyPressed(event, gameData)
        redrawScreenWrapper(canvas, gameData) # need to update player movement

    def updateGameWrapper(canvas, gameData):
        updateGame(canvas, gameData)
        redrawScreenWrapper(canvas, gameData)
        # set in time so the game doesn't move too fast
        canvas.after(50, updateGameWrapper, canvas, gameData) # delay game by 60 ms


    # initialize our object, CMU recommends to do a generic object, but would a class work in this case?
    gameData = EscapeSalGame()
    root = Toplevel() # draw the game box
    # initializeData(root) if we are going the generic object route, should already be initialized for class
    # wg = EscapeSalGUI(mode) didnt use this method because encountered chicken and egg problem??

    # CMU Tkinter recommends to use Canvas over grids for more comeplex moveable games
    canvas = Canvas(root, width=550, height=400)
    canvas.pack() # also couldn't get grids to works and found more tutorials on canvas

    # bind Keys/Button to Mouse from Miller's slides, honestly looked up how to do lambdas
    root.bind("<Button-1>", lambda event: mouseClickedWrapper(event, canvas, gameData))
    root.bind("<Key>", lambda event: keyPressedWrapper(event, canvas, gameData))

    updateGameWrapper(canvas, gameData)

    # allows the GUI to stay on the screen
    root.mainloop()
    print("Successfully quit!")


run()