#!/usr/bin/python

from tkinter import *
from tkinter import ttk
from tkinter import font
from time import sleep
import os, signal, time, datetime
import RPi.GPIO as GPIO

countbuttonpushes = 0
numSeconds = 120
fontSize = 240

Button=24 #GPIO 24 pin for Button
Buzzer=12 #GPIO 12 pin for Buzzer

#Setup GPIO interfaces and pins
GPIO.setwarnings(False) 
GPIO.setmode(GPIO.BCM)
GPIO.setup(Button,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(Buzzer,GPIO.OUT,initial=GPIO.LOW)

########################################################################################################################
#Functions
########################################################################################################################

def quit(*args):
    root.destroy()                      # Cleans up tkinter
    sleep(1)                            # sleep commands allow the pi to process
    GPIO.cleanup()                      # Clean up the GPIO Pins
    sleep(1)                            # sleep commands allow the pi to process
    os.kill(os.getpid(),signal.SIGTERM) # Kills PI process aka no hanging
            
    
def show_time():        
    GPIO.remove_event_detect(Button) # Remove the ability to queue up the button pushes during countdown
    for t in range(numSeconds, -1, -1):
            txt.set("{:02d}:{:02d}".format(*divmod(t, 60)))
            root.update()         
            # delay one second
            time.sleep(1)
                        
    GPIO.add_event_detect(Button,GPIO.RISING,callback=btnPush, bouncetime=1200) # Add back the button event so that we can detect it       
    GPIO.output(Buzzer,GPIO.HIGH)
            
def btnPush(stuff):
        global countbuttonpushes
        
        countbuttonpushes += 1 # counts the number of button pushes
        
        if (countbuttonpushes == 1):  # start the countdown         
            root.after(150, show_time) 
        elif (countbuttonpushes ==2): # Reset the clock to the starting time, reset button counter and Turn off Buzzer
            countbuttonpushes = 0
            GPIO.output(Buzzer,GPIO.LOW)
            txt.set("{:02d}:{:02d}".format(*divmod(numSeconds, 60))) # format time
            root.update() 
########################################################################################################################
#MAIN PROGRAM
########################################################################################################################

# Setup the Button interrupt
GPIO.add_event_detect(Button,GPIO.RISING,callback=btnPush, bouncetime=1200)

# Use tkinter lib for showing the clock
root = Tk()
root.attributes("-fullscreen", True)
root.configure(background='black')
root.bind("x", quit)

# Display Counters on the screen
txt = StringVar()
txt.set("{:02d}:{:02d}".format(*divmod(numSeconds, 60)))
fnt = font.Font(family='Helvetica', size=fontSize, weight='bold')
lbl = ttk.Label(root, textvariable=txt, font=fnt, foreground="red", background="black")
lbl.place(relx=0.5, rely=0.5, anchor=CENTER)

root.mainloop()

