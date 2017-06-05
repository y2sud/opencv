#Make the images more dark

import cv2
import os, logging,  re
#import cv2.cv as cv
import numpy as np
from matplotlib import pyplot as plt
import math

#mypath = "D:\\Hadoop\\Deep learning\\Latest v0.1\\1 page\\"
mypath = "D:\\2017\\deep-learning\\Latest v0.1\\1 page\\"

os.chdir(mypath)

image_files = []
inv = True

#nm = 'number_10'

def main(image_file):
    image = cv2.imread(image_file, cv2.IMREAD_GRAYSCALE)
    
    if inv:
        pass
    else:
        #image = cv2.bitwise_not(image)
        pass



    #cv2.imwrite('slant.jpg',img2)

    ret,th0 = cv2.threshold(image,220,255,cv2.THRESH_TOZERO_INV)
    if inv:
        ret,th1 = cv2.threshold(image,210,255,cv2.THRESH_BINARY_INV )
    else:
        ret,th1 = cv2.threshold(image,24,255,cv2.THRESH_BINARY )

    equ = cv2.equalizeHist(th0)

    th2 = cv2.adaptiveThreshold(image,255,cv2.ADAPTIVE_THRESH_MEAN_C,\
                cv2.THRESH_BINARY_INV,11,2)
    th3 = cv2.adaptiveThreshold(image,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
                cv2.THRESH_BINARY_INV,11,2)

    titles = ['orig','thresh','mean','gaussian','th0','contrast']

    #th2 = cv2.bitwise_not(th2)
    #th3 = cv2.bitwise_not(th3)
    
    images = [image,th1,th2,th3,th0,equ]

    if inv:
        outfile = ''.join(('thinv_',image_file))
    else:
        outfile = ''.join(('th_',image_file))

    #outfile = os.path.join(root, outfile)
    print 'outfile: ' , outfile
    cv2.imwrite(outfile,th1)

    for i in range(len(titles)):
        plt.subplot(2,3,i+1),plt.imshow(images[i],'gray')
        plt.title(titles[i])
        plt.xticks([]),plt.yticks([])

    #plt.subplot(2,3,i+2),plt.imshow(equ,'gray')
    #plt.show()



#print(args.dir)
for root, dirs, files in os.walk(mypath):
    #os.chdir(root)
    #print root
    #print files
    for file in files:
        #print file
        if re.search('(^number_.*).jpg', file):
            image_files.append(file)
            #image_files.append(os.path.join(root, file))

if (len(image_files) == 0):
    logging.error('No input file find so cannot continue')
    exit()


for image_file in image_files:
    #print image_file
    main(image_file)

