import json
import tkinter as tk
from sys import argv
from time import sleep
from tkinter import *
from tkinter import messagebox

from PIL import Image, ImageTk

# Accepts the image path from launch arguments, if no arguments are given it will display an error
try:
    filepath = str(argv[1])
except IndexError:
    tk.messagebox.showerror("Improper launch", "Please launch the program from the file context menu!")
    exit()

# Loads in settings for the program
settings = open("settings.json")
settings = json.load(settings)

# Loads the image into PIL and extracts image size (X,Y) for later manipulation
PIL_image = Image.open(filepath)
X, Y = PIL_image.size
PIL_image.close()   # Unloads the image

# Changes image sizes X and Y so they stay within a specified range (maxsize, minsize).
maxsize = settings['MaxImageSize']  # Assings value from settings.json to maxsize
minsize = settings['MinImageSize']  # same but to minsize
global ratio
if X > Y:
    ratio = X / Y
    if X > maxsize:
        X = maxsize
        Y = round(int(maxsize / ratio))
    elif X < minsize:
        X = minsize
        Y = round(int(500/ratio))
elif Y >= X:
    ratio = X / Y
    if Y > maxsize:
        Y = round(int(maxsize / ratio))
        X = maxsize
    elif Y < minsize:
        Y = round(int(minsize / ratio))
        X = minsize

# The class that contains everything
class Win(tk.Tk):
    def __init__(self):
        super().__init__()
        super().overrideredirect(True)  # Removes borders from the window
        super().attributes('-topmost', True)    # Makes sure the window stays on top
        super().geometry(f"{X}x{Y}")    # Sets window size to reflect that of the image (X, Y)

        global i, increment, minzoomsize    # Loads specific settings and makes them global
        i = settings['ZoomIncrement']
        increment = int(i * ratio)      # Calculates the increments in which to resize the image
        minzoomsize = settings['MinZoomSize']

        # Code that opens and resizes the image
        self.image = Image.open(filepath)
        self.image0 = self.image.resize((X, Y))
        self.image0 = ImageTk.PhotoImage(self.image0)
        self.label = tk.Label(self, image=self.image0)
        self.label.pack()

        self._offsetx = 0
        self._offsety = 0

        # Binds button controls to methods
        super().bind("<Button-1>", self.clickwin)
        super().bind("<B1-Motion>", self.dragwin)
        super().bind("<MouseWheel>", self.scrollwin)
        super().bind("<Button-3>", self.closewin)

    # Method bound to right-click that handles exiting the program
    @staticmethod
    def closewin(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            root.destroy()
            exit()

    # Method bound to left-click and mouse motion that handles calculating the offset when dragging the window
    def dragwin(self, event):
        x = super().winfo_pointerx() - self._offsetx
        y = super().winfo_pointery() - self._offsety
        super().geometry(f"+{x}+{y}")

    # Method bound to left-click that triggers the start of the window movement
    def clickwin(self, event):
        self._offsetx = super().winfo_pointerx() - super().winfo_rootx()
        self._offsety = super().winfo_pointery() - super().winfo_rooty()

    # Method bound to scroll-wheel that handles the resizing of the window and image (zooming in and out)
    def scrollwin(self, event):
        # Grab the size of the window
        width = self.winfo_width()
        height = self.winfo_height()

        if event.num == 5 or event.delta == -120:   # If mousewheel-down
            width -= increment
            height = int(width/ratio)
        if event.num == 4 or event.delta == 120:    # If mousewheel-up
            width += increment
            height = int(width/ratio)

        # Makes sure the window cannot be downsized into oblivion
        if width < minzoomsize:
            width = minzoomsize
            height = int(width/ratio)

        # Handles resizing of the image itself
        self.image0 = self.image.resize((width, height))
        self.image0 = ImageTk.PhotoImage(self.image0)

        sleep(0.01)     # remove if too slow, adds dealy to smooth out the stuttering

        self.label['image'] = self.image0   # updates the image on the label
        super().geometry(f"{width}x{height}")   # changest the window geometry

root = Win()    # Initializes the class
root.mainloop()
