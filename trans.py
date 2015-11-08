#translation

'''A simple program to take a series of images of the same sample, and align them.
The goal is to make it easier to view movies of the sample'''

import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure

import Tkinter as tk
import argparse
import numpy as np
import pims
from skimage import data, color
from skimage.draw import circle_perimeter
#Take FileName of image

parser = argparse.ArgumentParser(description='Translation')
parser.add_argument('filename', help="Input base file name of image sequence")
args = parser.parse_args()


#Begin GUI
root = tk.Tk()
f = Figure(figsize=(16,9))
#Load image for Defect Detection
frames = pims.ImageSequence(args.filename)
a=f.add_subplot(121)
a2=f.add_subplot(122)

i=0
def nextimage(i):
    a2.imshow(frames[i],cmap='gray')
    f.canvas.draw()
    i=i+1
    return
buttonnext = tk.Button(root, text="next",command=nextimage(i))
buttonnext.pack(side=tk.BOTTOM)

imax= a.imshow(frames[0],cmap='gray')
canvas = FigureCanvasTkAgg(f,master=root)
canvas.show()
canvas.get_tk_widget().pack(side=tk.TOP,fill=tk.BOTH,expand=1)
a2.imshow(frames[0],cmap='gray')
f.canvas.draw()
#for frame in frames[1:]:
#    a2.imshow(frame,cmap='gray')
#    f.canvas.draw()
#    print "oh"
toolbar = NavigationToolbar2TkAgg(canvas, root)
toolbar.update()
canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

toolbar

root.mainloop()
