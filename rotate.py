'''rotate.py takes in an image sequence of a sample being physically rotated through
some angle. Then, it preforms a reverse rotation, so that all the images have
the same orientation. This is useful if the experimentalist just wants to focus on 
light intensity changes as a function of rotation, and doesn't want to get
distracted.'''

import argparse
import matplotlib.pyplot as plt
import numpy as np
import math
import glob
from scipy.ndimage.interpolation import rotate
import os 
#Take FileName of image

#Create Folder to store rotated images
if not os.path.exists("./rotatedImages"):
    os.makedirs("./rotatedImages")
#Choose the reference file
parser = argparse.ArgumentParser(description='Rotation')
parser.add_argument('filename', help="Input file name of image")
args = parser.parse_args()
refImage = plt.imread(args.filename)

names = glob.glob('./*.tif')
frames =[plt.imread(name) for name in names]
#Now, we need to extract the rotation information from the filename.
f, (ax1,ax2) = plt.subplots(ncols=2, nrows=1, figsize=(10,5))
ax1.imshow(refImage,cmap='gray')
ax1.set_xlabel(args.filename)
angle = []
for name,frame in zip(names,frames):
    nextFrame = False
    print "Image "+name.strip("./")
    while nextFrame == False:
        ax2.cla()
        ax2.imshow(frame,cmap='gray')
        ax2.set_xlabel(name)
        plt.show()
        theta = input( "What is the angle of the rotation stage for this image?")
        angle = np.append(angle,float(theta))
        rotated = rotate(frame,float(theta),reshape=True)
        ax2.cla()
        ax2.imshow(rotated,cmap='gray')
        plt.show()
        conditionNext = input("Try again? y/n ")
        if conditionNext == 'n':
            nextFrame == True
    plt.imsave("./rotatedImages/rotated-"+name.strip("./"),rotated, vmin=None,cmap='gray')

