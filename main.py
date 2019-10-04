from tkinter import *
from tkinter import ttk
from tkinter import font
import time
import datetime

global endTime 

def quit(*args):
    root.destroy()
    
def show_time():
     for t in range(numSeconds, -1, -1):
        # format as 2 digit integers, fills with zero to the left
        # divmod() gives minutes, seconds
        sf = "{:02d}:{:02d}".format(*divmod(t, 60))
        #print(sf)  # test
        txt.set(sf)
        root.update()
        # delay one second
        time.sleep(1)

# Use tkinter lib for showing the clock
root = Tk()
root.attributes("-fullscreen", True)
root.configure(background='black')
root.bind("x", quit)
root.after(1000, show_time)

# Set the end date and time for the countdown
numSeconds = 120

fnt = font.Font(family='Helvetica', size=240, weight='bold')
txt = StringVar()
lbl = ttk.Label(root, textvariable=txt, font=fnt, foreground="red", background="black")
lbl.place(relx=0.5, rely=0.5, anchor=CENTER)

root.mainloop()
