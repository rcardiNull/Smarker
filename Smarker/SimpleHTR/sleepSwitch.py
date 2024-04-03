#!/usr/bin/env python
"""
This in an executable file.
This file will engage XSCREENSAVER and shutdown automation.sh file for the sleep mode.
call it from init.d  file
"""

import RPi.GPIO as GPIO
from time import sleep
import os
import subprocess
import psutil

def startSaver(channel):
    print("Starting Screen Saver")
    os.system('xscreensaver-command -activate') # start screen saver

def killSaver(channel):
    print("Kill the Screen Saver")
    os.system('xscreensaver-command -deactivate') # immitates user activity to stop xscreen saver

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(6,GPIO.IN,pull_up_down=GPIO.PUD_UP) # initially up
GPIO.add_event_detect(6,GPIO.FALLING,callback=killSaver)

GPIO.setup(5,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(5,GPIO.FALLING,callback=startSaver)

try:
    while True:
        sleep(0.1)
except KeyboardInterrupt:
    GPIO.cleanup()
