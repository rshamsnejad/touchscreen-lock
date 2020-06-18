#!/usr/bin/python

############################### SYSTEM MODULES #################################

import os
CURRENT_DIR = os.path.dirname(os.path.realpath(__file__)) + '/'

import sys

############################ GLOBAL VARIABLES ##################################

LockImagePath = CURRENT_DIR + 'pictures/padlock.gif'

LockScreenDisplayed = False

LockButtonNumber = 3 # Default GPIO input
LockButtonBounceTime = 0.1 # Default bounce time in s
LockButtonHoldTime = 2 # Default long press time in s

LockKeys = 'ctrl+shift+alt+l'
KeyboardActive = False

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

def die(Message):
    sys.stderr.write("ERROR : " + Message + '\n')
    sys.exit(1)

############################## CLI ARGUMENT PARSING ###########################

import argparse

CLIParser = argparse.ArgumentParser(
    description="Raspberry Pi Touschreen Lock Screen"
)

CLIParser.add_argument(
    "-k", "--keyboard",
    action="store",
    type=str,
    nargs='?',
    default="",
    const=LockKeys,
    metavar="KEY_COMBINATION",
    help="Use key combination to toggle the lock screen. \
    Default is Ctrl+Shift+Alt+L, and a custom combination can be specified."
)
CLIParser.add_argument(
    "-g", "--gpi",
    action="store",
    type=int,
    choices=range(0, 27),
    default=LockButtonNumber,
    metavar="[0-27]",
    help="Custom GPI pin to use in the BCM numbering system. \
    Default is GPIO 3."
)
CLIParser.add_argument(
    "-b", "--bounce-time",
    action="store",
    type=float,
    default=LockButtonBounceTime,
    help="Bounce time in seconds. Default is 0.1s."
)
CLIParser.add_argument(
    "-t", "--hold-time",
    action="store",
    type=float,
    default=LockButtonHoldTime,
    help="Long press time in seconds. Default is 2s."
)
CLIParser.add_argument(
    "-p", "--picture",
    action="store",
    type=str,
    default=LockImagePath,
    help="Path to custom picture. Only GIF and PGM/PPM are supported."
)

CLIArguments = CLIParser.parse_args()

if CLIArguments.keyboard:
    KeyboardActive = True
    # TODO : How to check input sanity ?
LockKeys=CLIArguments.keyboard

LockButtonNumber = CLIArguments.gpi

if CLIArguments.bounce_time >= 0:
    LockButtonBounceTime = CLIArguments.bounce_time
else:
    die("Invalid bounce time")

if CLIArguments.hold_time >= 0:
    LockButtonHoldTime = CLIArguments.hold_time
else:
    die("Invalid hold time")


if os.access(CLIArguments.picture, os.R_OK):
    FileName, FileExtension = os.path.splitext(CLIArguments.picture)
    if FileExtension in (".gif", ".pgm", ".ppm"):
        LockImagePath = CLIArguments.picture
    else:
        die("Wrong picture format. Only GIF and PGM/PPM are supported.")
else:
    die("Can't read file : " + CLIArguments.picture)

########################## GUI AND INPUT MODULES ###############################

if sys.version_info.major == 2: # We are using Python 2.x
    import Tkinter as tk
elif sys.version_info.major == 3: # We are using Python 3.x
    import tkinter as tk

import gpiozero

sys.path.append(CURRENT_DIR + 'libraries')
if KeyboardActive:
    import keyboard

################################################################################

# ---------------------------------------------------------------------------- #

################################### MAIN #######################################

RootLockScreen = tk.Tk()

LockImage = tk.PhotoImage(file=LockImagePath)

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
