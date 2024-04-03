from magicgui import magicgui
import time
import RPi.GPIO as GPIO
from picamera import PiCamera

#camera = PiCamera()
print('Starting CLock')

def clock():

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

