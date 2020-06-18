#!/usr/bin/python

############################### SYSTEM MODULES #################################

import os
CURRENT_DIR = os.path.dirname(os.path.realpath(__file__)) + '/'

import sys

############################### CLI ARGUMENT PARSING ###########################

import getopt

argument_list = sys.argv[1:]
short_options = "k:g:b:t:p:h"
long_options = ["keyboard=", "gpio=", "bounce-time=", "hold-time=", "picture=", "help"]

try:
    arguments, values = getopt.getopt(
        argument_list,
        short_options,
        long_options
    )
except getopt.error as err:
    print(str(err))
    sys.exit(2)

############################ GLOBAL VARIABLES ##################################

LockImagePath = CURRENT_DIR + 'pictures/padlock.gif'

LockScreenDisplayed = False

LockButtonNumber = 3 # Default GPIO input
LockButtonBounceTime = 0.1 # Default bounce time in s
LockButtonHoldTime = 2 # Default long press time in s

LockKeys = 'ctrl+shift+alt+l'
KeyboardActive = False

for current_argument, current_value in arguments:

    if current_argument in ("-k", "--keyboard"):
        KeyboardActive = True
        InputString = str(current_value)
        # TODO : How to check input sanity ?
        if InputString != "":
            LockKeys = InputString

    elif current_argument in ("-g", "--gpio"):
        InputNumber = int(current_value)
        if 0 <= InputNumber <= 26:
            LockButtonNumber = InputNumber
        else:
            die("Invalid GPIO pin")
            
    elif current_argument in ("-b", "--bounce-time"):
        InputNumber = float(current_value)
        if InputNumber >= 0:
            LockButtonBounceTime = InputNumber
        else:
            die("Invalid bounce time")

    elif current_argument in ("-t", "--hold-time"):
        InputNumber = float(current_value)
        if InputNumber >= 0:
            LockButtonHoldTime = InputNumber
        else:
            die("Invalid hold time")

    elif current_argument in ("-l", "--lock-keys"):
        InputString = str(current_value)
        # TODO : How to check input sanity ?
        LockKeys = InputString

    elif current_argument in ("-p" , "--picture"):
        InputString = str(current_value)
        if os.access(InputString, os.R_OK):
            FileName, FileExtension = os.path.splitext(InputString)
            if FileExtension in (".gif", ".pgm", ".ppm"):
                LockImagePath = InputString
            else:
                die("Wrong picture format. Only GIF and PGM/PPM are supported.")
        else:
            die("Can't read file : " + InputString)

    elif current_argument in ("-h", "--help"):
        printHelp()
        sys.exit(0)

    else:
        sys.stderr.write("ERROR : Unknown parameter.")
        printHelp()
        sys.exit(1)

########################## GUI AND INPUT MODULES ###############################

if sys.version_info.major == 2: # We are using Python 2.x
    import Tkinter as tk
elif sys.version_info.major == 3: # We are using Python 3.x
    import tkinter as tk

import gpiozero

sys.path.append(CURRENT_DIR + 'libraries')
if KeyboardActive:
    import keyboard

############################## FUNCTIONS #######################################

def setLockScreen(RootWindow, ImageToDisplay):
    # Root attributes
    RootWindow.attributes('-type', 'normal')
    RootWindow.attributes('-alpha', 0.5) # 50% global transparency
    RootWindow.attributes('-fullscreen', 'True')

    # Escape key to quit
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
    sys.stderr.write(Message)
    sys.exit(1)

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
