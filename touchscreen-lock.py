#!/usr/bin/python

############################### SYSTEM MODULES #################################

import os
CURRENT_DIR = os.path.dirname(os.path.realpath(__file__)) + '/'

import sys

############################### CLI ARGUMENT PARSING ###########################

import getopt

argument_list = sys.argv[1:]
short_options = "k"
long_options = "keyboard"

try:
    arguments, values = getopt.getopt(
        argument_list,
        short_options,
        long_options
    )
except getopt.error as err:
    print(str(err))
    sys.exit(2)

KeyboardActive = False
for current_argument, current_value in arguments:
    if current_argument in ("-k", "--keyboard"):
        KeyboardActive = True

########################## GUI AND INPUT MODULES ###############################

if sys.version_info.major == 2: # We are using Python 2.x
    import Tkinter as tk
elif sys.version_info.major == 3: # We are using Python 3.x
    import tkinter as tk

import gpiozero

sys.path.append(CURRENT_DIR + 'libraries')
if KeyboardActive:
    import keyboard

############################ GLOBAL VARIABLES ##################################

RootLockScreen = tk.Tk()
LockScreenDisplayed = False

#### Below variables can be customized to fit your needs

LockImagePath = CURRENT_DIR + 'pictures/padlock.gif'
LockImage = tk.PhotoImage(file=LockImagePath)

LockButtonNumber = 3 # GPIO 3 is the Lock button
LockButtonBounceTime = 0.1 # Bounce time in s
LockButtonHoldTime = 2 # Long press time in s

if KeyboardActive:
    LockKeys = 'ctrl+shift+alt+l'

############################## FUNCTIONS #######################################

def setLockScreen(RootWindow, ImageToDisplay):
    # Root attributes
    RootWindow.attributes('-type', 'normal')
    RootWindow.attributes('-alpha', 0.5) # 50% global transparency
    RootWindow.attributes('-fullscreen', 'True')

    # Escape key to quit
    global KeyboardActive
    if KeyboardActive:
        RootWindow.bind(
            "<Escape>",
            lambda e: (e.widget.withdraw(), e.widget.quit())
        )

    # Fullscreen dimensions
    w, h = RootWindow.winfo_screenwidth(), RootWindow.winfo_screenheight()

    # Set root fullscreen
    RootWindow.geometry("%dx%d+0+0" % (w, h))

    # Set canvas fullroot
    LockScreenCanvas = tk.Canvas(RootWindow, width=w, height=h)
    LockScreenCanvas.pack()
    LockScreenCanvas.configure(background='white')

    # Display image in canvas
    ImageSprite = LockScreenCanvas.create_image(w/2, h/2, image=ImageToDisplay)

    # Take focus and start
    RootWindow.focus_set()

def toggleLockScreen(LockScreenToToggle):
    global LockScreenDisplayed
    if LockScreenDisplayed:
        LockScreenToToggle.withdraw()
        # print("HIDDEN")
        LockScreenDisplayed = False
    else:
        LockScreenToToggle.deiconify()
        # print("SHOWN")
        LockScreenDisplayed = True

################################################################################

# ---------------------------------------------------------------------------- #

################################### MAIN #######################################

setLockScreen(RootLockScreen, LockImage)
RootLockScreen.withdraw() # Start hidden

## Lock screen triggers : keyboard + GPIO
if KeyboardActive:
    keyboard.add_hotkey(
        LockKeys,
        toggleLockScreen,
        args=[RootLockScreen]
    )

LockButton = gpiozero.Button(
    LockButtonNumber,
    pull_up=True,
    bounce_time=LockButtonBounceTime,
    hold_time=LockButtonHoldTime
)
LockButton.when_held = lambda: toggleLockScreen(RootLockScreen)

RootLockScreen.mainloop()
