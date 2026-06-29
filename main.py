# Import all required libraries
from random import randint
import PIL
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

# Goes to a position in a grid with x1,x2,y1,y2 defining the corners
def moveGrid(x,y,gridIn):
    xSpacing = (gridIn[1] - gridIn[0]) / gridIn[4]
    ySpacing = (gridIn[3] - gridIn[2]) / gridIn[5]
    xgo = math.floor(gridIn[0] + xSpacing * (x + 0.5))
    ygo = math.floor(gridIn[2] + ySpacing * (y + 0.5))
    pydirectinput.moveTo(xgo,ygo)

# Sets the failsafe delay to 0 while keeping the corner breakout
def setupFailsafes():
    pydirectinput.FAILSAFE = True
    pydirectinput.PAUSE = 0

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
grid = [x1,x2,y1,y2,width,hieght]

# Add a small amount of delay
print("Beginning sequence in 2 seconds")
time.sleep(2)

# Perform the solver on the grid (currently tests the movement function over 10 positions)
for i in range(0,1000):
    moveGrid(randint(0,23),randint(0,19),grid)
    time.sleep(1)