import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk
import sys
from tkinter import messagebox
# Accepts the image path
filepath = str(sys.argv[1])

# Creates the filename
name = filepath.split('\\')
name = name[-1]

# Loads the image into PIL for data extraction
PIL_image = Image.open(filepath)
X, Y = PIL_image.size
PIL_image.close()   # Unloads the image

# Changes X, Y to use later for resizing image and window to stay within certain size
if X > Y:
    ratio = X / Y
    if X > 1000:
        X = 1000
        Y = round(int(1000/ratio))
    elif X < 300:
        X = 300
        Y = round(int(100/ratio))
elif Y >= X:
    ratio = Y/X
    if Y > 1000:
        Y = 1000
        X = round(int(1000/ratio))
    elif Y < 300:
        Y = 300
        X = round(int(100/ratio))

class Win(tk.Tk):
    def __init__(self):
        super().__init__()
        super().overrideredirect(True)
        super().attributes('-topmost', True)

        self._offsetx = 0
        self._offsety = 0
        super().bind("<Button-1>", self.clickwin)
        super().bind("<B1-Motion>", self.dragwin)

    def dragwin(self, event):
        x = super().winfo_pointerx() - self._offsetx
        y = super().winfo_pointery() - self._offsety
        super().geometry(f"+{x}+{y}")

    def clickwin(self, event):
        self._offsetx = super().winfo_pointerx() - super().winfo_rootx()
        self._offsety = super().winfo_pointery() - super().winfo_rooty()

root = Win()
root.geometry(f'{X}x{Y}')

canvas = tk.Canvas(root, width=X, height=Y)
canvas.pack()
image1 = Image.open(filepath)
image1 = image1.resize((X, Y))
image = ImageTk.PhotoImage(image1)
canvas.create_image(0, 0, anchor=NW, image=image)

def close(self):
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        root.destroy()

canvas.bind("<Button-3>", close)

root.mainloop()
