from random import randint

import PIL
import pyscreeze
import pyautogui
import pydirectinput
import pydirectinput as direct
import time

'''
Top left: -1172 808
Bottom right: -766 1124
'''

'''
while True:
    xp, xy = pyautogui.position()
    print(str(pyautogui.position()) + "\n" + str(pyautogui.pixel(xp,xy)))
'''

#Get the two important coordianates
input("Hit enter when you are ready for top left corner")
x1, y1 = pyautogui.position()
print("Top left set to: " + str(x1) + " " + str(y1))
input("Hit enter when you are ready for bottom right corner")
x2, y2 = pyautogui.position()
print("Bottom right set to: " + str(x2) + " " + str(y2))

def grid(x,y):
    #print("Trying to move to x: " + str(x) + " y: " + str(y))
    xgo = x1 + ((x-1) * ((x2-x1) / 9))
    ygo = y1 + ((y-1) * ((y2-y1) / 7))
    xgo = round(xgo)
    ygo = round(ygo)
    #print("Moving to: " + str(xgo) + " " + str(ygo))
    pydirectinput.moveTo(xgo,ygo)

pydirectinput.FAILSAFE = True
pydirectinput.PAUSE = 0

print("Beginning sequence in 2 seconds")
time.sleep(2)