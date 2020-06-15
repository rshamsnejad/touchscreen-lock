#!/usr/bin/python

from sys import version_info
if version_info.major == 2:
    # We are using Python 2.x
    import Tkinter as tk
elif version_info.major == 3:
    # We are using Python 3.x
    import tkinter as tk

############################ Global variables ##################################

RootLockScreen = tk.Tk()

LockImagePath = './padlock.gif'
LockImage = tk.PhotoImage(file=LockImagePath)

################################################################################


############################ Functions #########################################

def setLockScreen(RootWindow, ImageToDisplay):

    # Root attributes
    RootWindow.attributes('-type', 'normal')
    RootWindow.attributes('-alpha', 0.5) # 50% global transparency
    RootWindow.attributes('-fullscreen', 'True')

    # Escape key to quit
    RootWindow.bind("<Escape>", lambda e: (e.widget.withdraw(), e.widget.quit()))

    # Fullscreen dimensions
    w, h = RootWindow.winfo_screenwidth(), RootWindow.winfo_screenheight()

    # Set root fullscreen
    RootWindow.geometry("%dx%d+0+0" % (w, h))

    # Set canvas fullroot
    LockScreenCanvas = tk.Canvas(RootWindow, width=w, height=h)
    LockScreenCanvas.pack()
    LockScreenCanvas.configure(background='white') # Empty string means transparent

    # Display image in canvas
    ImageSprite = LockScreenCanvas.create_image(w/2, h/2, image=ImageToDisplay)

    # Take focus and start
    RootWindow.focus_set()
    # RootWindow.mainloop()

    return RootWindow

################################################################################


################################ PROGRAM #######################################

LockScreen = setLockScreen(RootLockScreen, LockImage)

LockScreen.mainloop()
