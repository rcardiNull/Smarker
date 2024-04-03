

import datetime
import RPi.GPIO as GPIO
from time import sleep
from PIL import Image
from time import strftime
from gpiozero import Button
import os
import time 
import subprocess
import psutil
import sys

"""
RPiZero2: 
camera calling script with edited filepaths
12/25: added new file path bind with LineSegmentation folder

1/27: changing the shutter pin to GPIO17
3/12: program listens for the switch on pin5 to kill itself. 
4/3: add  xscreen saver deactivation with the shutterbutton press
     xscreen saver engages by itself. need to simulate mouse jib with a  shutter button
- xscreen-saver -deactivate
- getting rid of kill camera -> no longer needed due to xscreensaver activating outside of program
"""
# Event listener. 
# image capture function
i=0
print("Welcome to Camera Script: press the button")
def piselfie(channel):
    os.system('xscreensaver-command -deactivate') #stopped here: disabling screen saver on button press to display camera
    sleep(2)
    print('Camera: ON')
    global i
    sleep(2)
    print("Smile:___Taking a Photo___")
    photoName = 'newPhoto' +str(i)+ '.png'
    os.system("libcamera-still -t 5000 -o /home/pi2/camCombo/Smarker/SimpleHTR/LineSegmentation/sourceImg/"+photoName)
    print('Saving photo ',i, 'to file')
    i+=1

# GPIO settings
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(17,GPIO.IN,pull_up_down=GPIO.PUD_UP) # intially off
GPIO.add_event_detect(17,GPIO.FALLING,callback=piselfie)

try:
    while True:
         sleep(0.1) 
except KeyboardInterrupt:
    GPIO.cleanup()
