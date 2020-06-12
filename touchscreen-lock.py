#!/usr/bin/python

import tkinter
from PIL import Image, ImageTk

def showPIL(pilImage):

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

    # Set up image
    imgWidth, imgHeight = pilImage.size
    if imgWidth > w or imgHeight > h:
        ratio = min(w/imgWidth, h/imgHeight)
        imgWidth = int(imgWidth*ratio)
        imgHeight = int(imgHeight*ratio)
        pilImage = pilImage.resize((imgWidth, imgHeight), Image.ANTIALIAS)
    image = ImageTk.PhotoImage(pilImage)
    imagesprite = canvas.create_image(w/2, h/2, image=image)

    # Take focus and start
    root.focus_set()
    root.mainloop()

im = Image.open('./padlock.png')
showPIL(im)
