# Import all required libraries
import random
from linecache import checkcache
from random import randint
from PIL import ImageGrab
import pyscreeze
import pyautogui
import pydirectinput
import pydirectinput as direct
import time
import math

# Esentially halts the program
def infinitePause():
    while True:
        time.sleep(100)

# Displays the hovered over position on the screen
def getCoords():
    while True:
        xp, xy = pyautogui.position()
        print(str(pyautogui.position()) + "\n" + str(pyautogui.pixel(xp, xy)))

# Sets the failsafe delay to 0 while keeping the corner breakout
def setupFailsafes():
    pydirectinput.FAILSAFE = True
    pydirectinput.PAUSE = 0

# Converts grid positions into screen positions
def toPosition(x,y,gridIn,shiftX=0,shiftY=0):
    xSpacing = (gridIn[2] - gridIn[0]) / gridIn[4]
    ySpacing = (gridIn[3] - gridIn[1]) / gridIn[5]
    xout = math.floor(gridIn[0] + xSpacing * (x + 0.5 + shiftX))
    yout = math.floor(gridIn[1] + ySpacing * (y + 0.5 + shiftY))
    return xout, yout

# Goes to a position in a grid with x1,y1,x2,y2 defining the corners
def moveGrid(x,y,gridIn,shiftX=0,shiftY=0):
    xgo, ygo = toPosition(x,y,gridIn,shiftX,shiftY)
    pydirectinput.moveTo(xgo,ygo)

# Moves and clicks at a desired position
def moveClick(x,y,gridIn,shiftX=0,shiftY=0):
    moveGrid(x,y,gridIn,shiftX,shiftY)
    pydirectinput.click()

# Moves and right clicks at a desired position
def moveRightClick(x,y,gridIn,shiftX=0,shiftY=0):
    moveGrid(x,y,gridIn,shiftX,shiftY)
    pydirectinput.rightClick()

# Returns the color from the provided grid position in the screenshot
def grabColorGrid(x,y,gridIn,pixels,shiftX=0,shiftY=0):
    xTest, yTest = toPosition(x, y, gridIn, shiftX, shiftY)
    return pixels[xTest,yTest]

# Scans the board and determines what all of the squares are
def scanGrid(gridIn):
    pydirectinput.moveTo(0,0)
    img = ImageGrab.grab()
    img.save("testImage.png","PNG")
    pix = img.load()
    # Sets up the color variables (missing 5-8)
    lightGreen = (170, 215, 81)
    darkGreen = (162, 209, 73)
    lightTan = (229, 194, 159)
    darkTan = (215, 184, 153)
    one = (25, 118, 210)
    two = (56, 142, 60)
    three = (211, 47, 47)
    four = (123, 31, 162)
    five = (255, 143, 0)
    six = (0, 151, 167)
    seven = (66, 66, 66)
    # Scans over the image and traces those locations with the mouse
    checkXShift = 0.05
    checkYShift = 0.24
    checkXShift7 = 0
    checkYShift7 = 0
    board = []
    print("Scanning board:")
    for y in range(0,gridIn[5]):
        printRow = ""
        row = []
        for x in range(0,gridIn[4]):
            curColor = grabColorGrid(x, y, gridIn, pix, checkXShift, checkYShift)
            if curColor == lightGreen:
                printRow = printRow + "■"
                row.append(-1)
                delay = 0
            elif curColor == darkGreen:
                #printRow = printRow + "□"
                printRow = printRow + "■"
                row.append(-1)
                delay = 0
            elif curColor == lightTan or curColor == darkTan:
                printRow = printRow + "."
                row.append(0)
                delay = 0.25
            elif curColor == one:
                printRow = printRow + "1"
                row.append(1)
                delay = 0.25
            elif curColor == two:
                printRow = printRow + "2"
                row.append(2)
                delay = 0.25
            elif curColor == three:
                printRow = printRow + "3"
                row.append(3)
                delay = 0.25
            elif curColor == four:
                printRow = printRow + "4"
                row.append(4)
                delay = 0.25
            elif curColor == five:
                printRow = printRow + "5"
                row.append(5)
                delay = 0.25
            elif curColor == six:
                printRow = printRow + "6"
                row.append(6)
                delay = 0.25
            else:
                if grabColorGrid(x, y, gridIn, pix, checkXShift7, checkYShift7) == seven:
                    printRow = printRow + "7"
                    row.append(7)
                    delay = 0.25
                else:
                    printRow = printRow + "X"
                    row.append("Error with scan")
                    print("Failed to scan")
                    print("Failed color: " + str(curColor))
                    moveGrid(x, y, gridIn, checkXShift, checkYShift)
                    infinitePause()
                    delay = 1
            #moveGrid(x, y, gridIn, checkXShift, checkYShift) # Shows where the image is bieng checked, only works if the below delay line is uncommented
            #time.sleep(delay)
        print(printRow)
        board.append(row)
    #print(board)
    return board

# Waits until the destruction particles have gone away for a good scan
def waitForDebris():
    pydirectinput.moveTo(0,0)
    time.sleep(1)

# Prompt the user for the coordinates that are relevant for their screen
def getCorners():
    input("Hit enter when you are ready for top left corner")
    x1, y1 = pyautogui.position()
    print("Top left set to: " + str(x1) + " " + str(y1))
    input("Hit enter when you are ready for bottom right corner")
    x2, y2 = pyautogui.position()
    print("Bottom right set to: " + str(x2) + " " + str(y2))
    return x1, y1, x2, y2

# Using the grid and scanned board reports the tiles that are touching a number
def getEdgeTiles(gridIn,scannedBoardIn):
    edgeTiles = []
    for y in range(0, gridIn[5]):
        for x in range(0, gridIn[4]):
            if scannedBoardIn[y][x] == -1:
                valid = 0
                for direction in range(0,8):
                    denormalizedX = [0,1,1,1,0,-1,-1,-1]
                    denormalizedY = [1,1,0,-1,-1,-1,0,1]
                    emptyX = x + denormalizedX[direction]
                    emptyY = y + denormalizedY[direction]
                    if emptyX >= 0 and emptyX < gridIn[4] and emptyY >= 0 and emptyY < gridIn[5]:
                        if scannedBoardIn[emptyY][emptyX] != -1:
                            valid = 1
                if valid == 1:
                    edgeTiles.append([x,y])
    return edgeTiles

def boardArrayPrint(board):
    print("Printout of the board:")
    for y in range(0,len(board)):
        row = ""
        for x in range(0,len(board[0])):
            if board[y][x] == -1:
                row = row + "■"
            elif board[y][x] == 0:
                row = row + "."
            elif board[y][x] == 9:
                row = row + "B"
            else:
                row = row + str(board[y][x])
        print(row)
    print("")

# Notes on the minesweeper board dimensions
'''
Hard:
24 tiles wide (0-23)
20 tiles tall (0-19)
'''

# Ensure that the failsafes are configured correctly and active
setupFailsafes()

# Set up position variables and set their values
getTheCorners = input("Do you want to re-record the corners?")
if getTheCorners == "Y" or getTheCorners == "y" or getTheCorners == "Yes" or getTheCorners == "yes" or getTheCorners == "YES":
    x1, y1, x2, y2 = getCorners()
else:
    x1, y1, x2, y2 = 604, 267, 1937, 1378

# Define remaining size data and compact all of the values into a list for convinience
width = 24
hieght = 20
grid = [x1,y1,x2,y2,width,hieght]

# Add a small amount of delay to allow it to be watched comfortably
print("Beginning movement in 2 seconds.")
time.sleep(2)

# Click the center square to get things started
centerX = math.floor(width/2)
centerY = math.floor(hieght/2)
moveClick(centerX,centerY,grid)
waitForDebris()

# Scan the board to get the current state


# Solve the board in stages using simple rules
# 1: If a number is next to the same amount of blank tiles as its number, all of those are bombs
# 2: If a number already has the number of bombs next to it as its number, everything else is safe

bombPositions = []
somethingChanged = 1
while somethingChanged == 1:
    somethingChanged = 0

    # Scan the board and add back any bombs that have been identified
    scannedBoard = scanGrid(grid)
    bombBoard = scannedBoard.copy()
    for pos in bombPositions:
        x, y = pos
        bombBoard[y][x] = 9

    # Rule 1
    for y in range(0, grid[5]):
        for x in range(0, grid[4]):
            if bombBoard[y][x] in [1,2,3,4,5,6,7,8]:
                surroundingTiles = 0
                for direction in range(0, 8):
                    denormalizedX = [0, 1, 1, 1, 0, -1, -1, -1]
                    denormalizedY = [1, 1, 0, -1, -1, -1, 0, 1]
                    emptyX = x + denormalizedX[direction]
                    emptyY = y + denormalizedY[direction]
                    if emptyX >= 0 and emptyX < grid[4] and emptyY >= 0 and emptyY < grid[5]:
                        if bombBoard[emptyY][emptyX] in [-1,9]:
                            surroundingTiles = surroundingTiles + 1
                if surroundingTiles == bombBoard[y][x]:
                    for direction in range(0, 8):
                        denormalizedX = [0, 1, 1, 1, 0, -1, -1, -1]
                        denormalizedY = [1, 1, 0, -1, -1, -1, 0, 1]
                        emptyX = x + denormalizedX[direction]
                        emptyY = y + denormalizedY[direction]
                        if emptyX >= 0 and emptyX < grid[4] and emptyY >= 0 and emptyY < grid[5]:
                            if bombBoard[emptyY][emptyX] == -1:
                                bombBoard[emptyY][emptyX] = 9
                                bombPositions.append([emptyX,emptyY])
                                moveRightClick(emptyX, emptyY, grid)
                                somethingChanged = 1

    # Rule 2
    for y in range(0, grid[5]):
        for x in range(0, grid[4]):
            if bombBoard[y][x] in [1,2,3,4,5,6,7,8]:
                surroundingBombs = 0
                for direction in range(0, 8):
                    denormalizedX = [0, 1, 1, 1, 0, -1, -1, -1]
                    denormalizedY = [1, 1, 0, -1, -1, -1, 0, 1]
                    emptyX = x + denormalizedX[direction]
                    emptyY = y + denormalizedY[direction]
                    if emptyX >= 0 and emptyX < grid[4] and emptyY >= 0 and emptyY < grid[5]:
                        if bombBoard[emptyY][emptyX] in [9]:
                            surroundingBombs = surroundingBombs + 1
                if surroundingBombs == bombBoard[y][x]:
                    for direction in range(0, 8):
                        denormalizedX = [0, 1, 1, 1, 0, -1, -1, -1]
                        denormalizedY = [1, 1, 0, -1, -1, -1, 0, 1]
                        emptyX = x + denormalizedX[direction]
                        emptyY = y + denormalizedY[direction]
                        if emptyX >= 0 and emptyX < grid[4] and emptyY >= 0 and emptyY < grid[5]:
                            if bombBoard[emptyY][emptyX] == -1:
                                moveClick(emptyX,emptyY,grid)
                                somethingChanged = 1

    # Guess randomly if nothing else works
    randomTiles = []
    if somethingChanged == 0:
        for y in range(0, grid[5]):
            for x in range(0, grid[4]):
                if bombBoard[y][x] == -1:
                    randomTiles.append([x,y])
        if len(randomTiles) != 0:
            x,y = random.choice(randomTiles)
            moveClick(x, y, grid)
            somethingChanged = 1

    # To prevent debris from messing up the scan
    waitForDebris()

# Print a debug board
boardArrayPrint(bombBoard)
