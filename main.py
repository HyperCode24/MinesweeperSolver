# Import all required libraries
from random import randint
import PIL
import pyscreeze
import pyautogui
import pydirectinput
import pydirectinput as direct
import time

# Displays the hovered over position on the screen
def getCoords():
    while True:
        xp, xy = pyautogui.position()
        print(str(pyautogui.position()) + "\n" + str(pyautogui.pixel(xp, xy)))

# Goes to a position in a grid with x1,x2,y1,y2 defining the corners
def grid(x,y):
    #print("Trying to move to x: " + str(x) + " y: " + str(y))
    xgo = x1 + ((x-1) * ((x2-x1) / 9))
    ygo = y1 + ((y-1) * ((y2-y1) / 7))
    xgo = round(xgo)
    ygo = round(ygo)
    #print("Moving to: " + str(xgo) + " " + str(ygo))
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

# Add a small amount of delay
print("Beginning sequence in 2 seconds")
time.sleep(2)

# Perform the solver on the grid (currently tests the movement function over 10 positions)
for i in range(0,10):
    grid(randint(0,23),randint(0,19))
    time.sleep(1)