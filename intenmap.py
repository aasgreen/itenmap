#Intensity Mapping Program

'''intenmap.py will provide a way for the user to select a point on an image,
then the program will plot the radial intensity of the image at a user-chosen
diameter. It will be designed to be easily extendable'''

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

parser = argparse.ArgumentParser(description='Defect Tracking')
parser.add_argument('filename', help="Input file name of image")
args = parser.parse_args()

#Begin GUI
root = tk.Tk()
f = Figure(figsize=(7,7),dpi=100)
#Load image for Defect Detection
frames = pims.ImageSequence(args.filename)

#Master image will be where we get our brightness data, display image will be
#able to display the circle that we are drawing
masterImage =frames[0]
displayImage = frames[0]
a=f.add_subplot(111)
#a2=f.add_subplot(212)
imax= a.imshow(displayImage,cmap='gray')
canvas = FigureCanvasTkAgg(f,master=root)
canvas.show()
canvas.get_tk_widget().pack(side=tk.TOP,fill=tk.BOTH,expand=1)
def callback(event):
    image = np.copy(displayImage)
    print "clicked at", event.xdata, event.ydata
    #Draw Circle of radius 50
    center_x, center_y = int(event.xdata), int(event.ydata)
    radius = 50
    print center_x, center_y
    cx,cy = circle_perimeter(center_x,center_y, radius)
   
    #Now get brightness data
    xNormalized = cx-center_x
    yNormalized = cy-center_y
#    angle = np.arctan2(yNormalized,xNormalized)
#    lumtest = masterImage[cy,cx]

    angle2 = np.linspace(0,2*np.pi,2000)
    lum = np.zeros(angle2.shape)
    lumError = np.zeros(angle2.shape)
    for i,theta in enumerate(angle2):
        xRange = np.linspace(radius-2,radius+2.,10)*np.cos(theta)+center_x
        yRange = np.linspace(radius-2,radius+2.,10)*np.sin(theta)+center_y
        #image[yRange.astype(int),xRange.astype(int)]=0 #visualize region of averaging
        lum[i] =masterImage[np.rint(yRange).astype(int),np.rint(xRange).astype(int)].mean()
        lumError[i]=masterImage[yRange.astype(int),xRange.astype(int)].std()
        image[np.rint(yRange).astype(int),np.rint(xRange).astype(int)]=0

#j    a2.cla()
 #   a2.errorbar(angle,lum, yerr=lumError,fmt='.')
#    image[cy,cx] = 0
    a.cla()
    imax= a.imshow(image,cmap='gray')
    f.canvas.draw()
 #   print image[cy,cx]
    answer = raw_input('Would you like to save this data? y/n ')
    print answer
    if answer == "y":
        saveName = raw_input("File save name. (Please label which feature, and which angle). ")
        np.savetxt(saveName,np.vstack( [angle2,lum,lumError]))
canvas.mpl_connect('button_press_event', callback)
toolbar = NavigationToolbar2TkAgg(canvas, root)
toolbar.update()
canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

toolbar

root.mainloop()
