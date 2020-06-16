#!/usr/bin/python

import sys
if sys.version_info.major == 2: # We are using Python 2.x
    import Tkinter as tk
elif sys.version_info.major == 3: # We are using Python 3.x
    import tkinter as tk

sys.path.append('libraries')
import keyboard
import gpiozero


############################ Global variables ##################################

RootLockScreen = tk.Tk()

LockImagePath = './padlock.gif'
LockImage = tk.PhotoImage(file=LockImagePath)

LockScreenDisplayed = False

LockButtonNumber = 3 # GPIO 3 is the Lock button
LockButtonBounceTime = 200 # Bounce time in ms
LockButtonHoldTime = 2 # Long press time

################################################################################


############################ Functions #########################################

def setLockScreen(RootWindow, ImageToDisplay):

    # Root attributes
    RootWindow.attributes('-type', 'normal')
    RootWindow.attributes('-alpha', 0.5) # 50% global transparency
    RootWindow.attributes('-fullscreen', 'True')

    # Escape key to quit
    RootWindow.bind("<Escape>", lambda e: (e.widget.withdraw(), e.widget.quit()))
    # RootWindow.bind("<Escape>", lambda e: (toggleLockScreen(RootWindow)))

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

def toggleLockScreen(Trigger, LockScreenToToggle):
    global LockScreenDisplayed
    if LockScreenDisplayed:
        LockScreenToToggle.withdraw()
        print("HIDDEN")
        LockScreenDisplayed = False
    else:
        LockScreenToToggle.deiconify()
        print("SHOWN")
        LockScreenDisplayed = True

################################################################################


################################ PROGRAM #######################################

setLockScreen(RootLockScreen, LockImage)
RootLockScreen.withdraw() # Start hidden

## Lock screen triggers : keyboard + GPIO
keyboard.add_hotkey('ctrl+shift+alt+l', toggleLockScreen, args=[False, RootLockScreen])

LockButton = gpiozero.Button(
    LockButtonNumber,
    pull_up=True,
    #active_state=False,
    bounce_time=LockButtonBounceTime,
    hold_time=LockButtonHoldTime
)

#LockButton.when_held = toggleLockScreen(LockButton, RootLockScreen)
#LockButton.when_released = toggleLockScreen(LockButton, RootLockScreen)

RootLockScreen.mainloop()

