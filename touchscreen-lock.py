#!/usr/bin/python

import tkinter

LockImage = './padlock.gif'

def showLockScreen(ImageToDisplay):

    root = tkinter.Tk()

    # Root attributes
    root.attributes('-type', 'normal')
    root.attributes('-alpha', 0.5) # 50% global transparency
    root.attributes('-fullscreen', 'True')

    # Escape key to quit
    root.bind("<Escape>", lambda e: (e.widget.withdraw(), e.widget.quit()))

    # Fullscreen dimensions
    w, h = root.winfo_screenwidth(), root.winfo_screenheight()

    # Set root fullscreen
    root.geometry("%dx%d+0+0" % (w, h))

    # Set canvas fullroot
    canvas = tkinter.Canvas(root, width=w, height=h)
    canvas.pack()
    canvas.configure(background='white') # Empty string means transparent

    # Display image in canvas
    image = tkinter.PhotoImage(file=ImageToDisplay)
    imagesprite = canvas.create_image(w/2, h/2, image=image)

    # Take focus and start
    root.focus_set()
    root.mainloop()

showLockScreen(LockImage)
