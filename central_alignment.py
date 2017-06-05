#Align the images centrally

import cv2
import os, logging,  re
#import cv2.cv as cv
import numpy as np
from matplotlib import pyplot as plt
import math

mypath = "D:\\2017\\deep-learning\\Latest v0.1\\1 page\\"
#mypath = "D:\\Hadoop\\Deep learning\\Latest v0.1\\7 page\\"

os.chdir(mypath)

image_files = []
inv = True

#nm = 'number_10'

class Center:
    LUMENS = 200
    COEF = 2
    ROWS, COLUMNS = 28, 28
    # The density/proportion of white pixels between left-half & right-half in cropped image should be between 35 to 65%. If it's outside this range then the image
    # has a long tail that needs to be trimmed
    LMARGIN , RMARGIN = 0.35 , 0.65
    # If image has a long tail, then how much % of cropped image should be retained is given by below parm
    PERCTRIM = 0.7
    
    def __init__(self,img):
        self.img = img
        self.top, self.left, self.right, self.bot = 999, 999, -999, -999

        #self.LUMENS = 200

    def findCords(self):
        h , w = self.img.shape
        top, left, right, bot = self.top, self.left, self.right, self.bot
        for row in range(h):
            for col in range(w):
                if self.img[row,col] > Center.LUMENS:
                    if top > row:
                        top = row
                    if left > col:
                        left = col
                    if right < col:
                        right = col
                    if bot < row:
                        bot = row
        self.top, self.left, self.right, self.bot = (top, left, right, bot)
        print 'top, left, right, bot ' , top, left, right, bot

    def fineTune(self,crop):
        #img = self.img
        h , w = crop.shape
        leftArr , rightArr = 0,0
        leftCrop, rightCrop = False, False
        print 'h , w ' , h ,w 
        mid = w / 2.0 - 1
        if (w % 2.0 == 0):
            even = True
        else:
            even = False
            mid = math.floor(mid)
        print 'Mid ' , mid
        
        for col in range(w):
            for row in range(h):
                if crop[row,col] >= 200:
                    #print 'col , row, mid ' , col , row, mid
                    if col <= mid:
                        leftArr += 1
                    else:
                        if even:
                            rightArr += 1
                        else:
                            if col == mid + 1:
                                break
                            else:
                                rightArr += 1
        tot = leftArr + rightArr
        print 'leftArr , rightArr, % ' , leftArr, rightArr , float(leftArr) / tot
        if float(leftArr) / tot < Center.LMARGIN:
            leftCrop = True
            print 'left % ' , float(leftArr) / tot , leftArr , tot
        if float(leftArr) / tot > Center.RMARGIN:
            rightCrop = True
            print 'right % ' , float(leftArr) / tot , leftArr, tot

        start , end = 0 , w-1
        if leftCrop:
            start = int(w - math.floor(Center.PERCTRIM * w))
            end = w
            self.left = start
            self.right = end
            
        if rightCrop:
            start = 0
            end = int(math.floor(Center.PERCTRIM * w))
            self.right = end
            self.left = start

        return crop[0:,start:end+1]
        
    def cropImg(self):
        crop = self.img[self.top:self.bot+1,self.left:self.right+1]
        cv2.imwrite('temp.jpg',crop)
        return crop
    
    def alignCenter(self,crop):
        h , w = crop.shape
        #row = Center.ROWS
        col = Center.COLUMNS
        row = Center.ROWS
        #row = h + Center.COEF
        
        if w >= col:
            col = w + Center.COEF        
        if h >= row:
            row = h + Center.COEF        
        
        im28x28 = np.zeros((row,col),dtype=np.int)
        length = self.bot - self.top + 1
        breadth = self.right - self.left + 1
        print self.left , self.right
        
        #diff = Center.ROWS - length
        diff = row - length
        offsetI = int(math.ceil(diff / 2.0))
        
        #diff = Center.COLUMNS - breadth
        diff = col - breadth
        offsetJ = int(math.ceil(diff / 2.0))
        print 'offset i,j ' , offsetI , offsetJ
        #h , w = crop.shape
        for i in range(h):
            ii = i + offsetI
            for j in range(w):
                jj = j + offsetJ
                im28x28[ii,jj] = crop[i,j]
        
        return im28x28

class Main():
    def __init__(self,mypath):
        self.mypath = mypath
        self.image_file = ''
        
    def mainPara(self):
        image_file = self.image_file
        image = cv2.imread(image_file, cv2.IMREAD_GRAYSCALE)
        #print image
        imgObj = Center(image)
        imgObj.findCords()
        crop = imgObj.cropImg()
        crop = imgObj.fineTune(crop)
        im28x28 = imgObj.alignCenter(crop)
        


    #    titles = ['orig','thresh','mean','gaussian','th0','contrast']
    #    images = [image,th1,th2,th3,th0,equ]

        outfile = ''.join(('crop_',image_file))
        outfile = os.path.join(self.mypath, outfile)

        cv2.imwrite(outfile,im28x28)
        
        print 'outfile: ' , outfile

    #    for i in range(len(titles)):
    #        plt.subplot(2,3,i+1),plt.imshow(images[i],'gray')
    #        plt.title(titles[i])
    #        plt.xticks([]),plt.yticks([])

        #plt.subplot(2,3,i+2),plt.imshow(equ,'gray')
    #    plt.show()


    def loop(self):
        #print(args.dir)
        for root, dirs, files in os.walk(self.mypath):
            #os.chdir(root)
            #print root
            #print files
            for file in files:
                #print file
                if re.search('(^thinv_.*).jpg', file):
                    image_files.append(file)
                    #image_files.append(os.path.join(root, file))

        if (len(image_files) == 0):
            logging.error('No input file find so cannot continue')
            exit()


        for image_file in image_files:
            print image_file
            self.image_file = image_file
            self.mainPara()


new = Main(mypath)
new.loop()

