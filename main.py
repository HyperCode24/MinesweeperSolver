# Import all required libraries
from random import randint
from PIL import ImageGrab
import pyscreeze
import pyautogui
import pydirectinput
import pydirectinput as direct
import time
import math

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

# Returns the color from the provided grid position in the screenshot
def grabColorGrid(x,y,gridIn,pixels,shiftX=0,shiftY=0):
    xTest, yTest = toPosition(0, 0, gridIn, shiftX, shiftY)
    return pixels[xTest,yTest]

# Scans the board and determines what all of the squares are
def scanGrid(gridIn):
    img = ImageGrab.grab()
    img.save("testImage.png","PNG")
    pix = img.load()
    print(grabColorGrid(0,0,gridIn,pix))

# Waits until the destruction particles have gone away for a good scan
def waitForDebris():
    time.sleep(1)

# Notes on the minesweeper board dimensions
'''
Hard:
24 tiles wide (0-23)
20 tiles tall (0-19)
'''

# Ensure that the failsafes are configured correctly and active
setupFailsafes()

# Prompt the user for the coordinates that are relevant for their screen
input("Hit enter when you are ready for top left corner")
x1, y1 = pyautogui.position()
print("Top left set to: " + str(x1) + " " + str(y1))
input("Hit enter when you are ready for bottom right corner")
x2, y2 = pyautogui.position()
print("Bottom right set to: " + str(x2) + " " + str(y2))

# Define remaining size data and compact all of the values into a list for convinience
width = 24
hieght = 20
grid = [x1,y1,x2,y2,width,hieght]

# Add a small amount of delay
print("Beginning sequence in 2 seconds")
time.sleep(2)

# Click the center square to get things started
centerX = math.floor(width/2)
centerY = math.floor(hieght/2)
moveClick(centerX,centerY,grid)
waitForDebris()
scanGrid(grid)