#!/usr/bin/python3
import tkinter as tk
import time
import RPi.GPIO as GPIO
"""
This script will start and stop the clock
8/26 clock call works at a click of a button:
will place this script to run at boot
"""

#clock_pin=17
#GPIO.setwarnings(False)
#GPIO.setmode(GPIO.BCM)
#GPIO.setup(clock_pin,GPIO.IN,pull_up_down=GPIO.PUD_UP)

try:
    #GPIO.wait_for_edge(clock_pin,GPIO.FALLING)
    print('Starting CLock')
    time.sleep(5)
    print("Started Clock")
    def timeClock():
        current_time=time.strftime("%H:%M:%S") 
        clock.config(text=current_time)
        clock.after(200,timeClock) 

    global r
    r=tk.Tk()
    r.geometry("800x480")
    r.configure(background='black')
    clock=tk.Label(r,font=("ds-digital",175,"bold"),bg="black",fg='cyan')
    clock.pack(anchor='center')
    clock.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
    timeClock() 
    r.mainloop()


except KeyboardInterrupt:
    print("CLeaning up")
    GPIO.cleanup()
