#De-skew the image

import cv2, re, sys, os
#import cv2.cv as cv
import numpy as np
from matplotlib import pyplot as plt
import math

mypath = "D:\\Hadoop\\Deep learning\\Latest v0.1\\7 page\\"
sys.chdir(mypath)

for root, dirs, files in os.walk(mypath):
    print files
    for file in files:
        if re.search('.*page.jpg$', file):
            img = cv2.imread(file, cv2.IMREAD_GRAYSCALE)
            exit()
    else:
        print 'FATAL : Not able to find *page.jpg file'
        sys.exit(1)
#img = cv2.imread('1.jpg', cv2.IMREAD_GRAYSCALE)

# make ithe image black & white
#ret, img = cv2.threshold(img,200,255,cv2.THRESH_TOZERO)
#img2 = img.copy()
#img2.resize(400,400)
#img = cv2.imread('1st page.jpg')

cntDictNeg = {}; valDictNeg = {}; cntDictPos = {}; valDictPos = {}

#CV_PI =  3.1415926535897932384626433832795

def compute_skew(image):
    #image = cv2.bitwise_not(image)
    height, width = image.shape

    edges = cv2.Canny(image, 10, 200, 3, 5)
    #print edges
    #lines = [1,2]
    lines = cv2.HoughLinesP(edges,1, np.pi/180.0, 25, minLineLength=width / 2.5, maxLineGap=20)
    #lines = cv2.HoughLines(edges,1, np.pi/180, 10)
    angle = neg_angle = pos_angle = 0.0
    neg_cnt = pos_cnt = 0
    #print lines
    #print type(lines)
    nlines, junk1, junk2 = lines.shape
    '''
    Two dictionaries each for positive & negative angles.
    One having floor(angle):count, other having floor(angle): sum of angles
    e.g., 6:4 & 6:26.2   ... say
    '''
    global cntDictNeg , valDictNeg , cntDictPos , valDictPos    

    # List of all angles
    mainList = []
    # Loop thru all lines
    for i in range(nlines):
        for x1, y1, x2, y2 in lines[i]:
            #print x1, y1, x2, y2
            # Angle in degrees
            angle = np.arctan2(y2-y1,x2 - x1) * 180 / np.pi
            if angle in ( 0.0, 90.0, -90.0):
                pass
            else:
                mainList.append(angle)
                if (angle < 0.0):
                    neg_cnt += 1
                    neg_angle += angle
                    buildDict(angle)
                else:
                    pos_cnt += 1
                    pos_angle += angle
                    buildDict(angle)
                    
            #print angle
            lineimg = cv2.line(image,(x1,y1),(x2,y2),(110,110,110),5)
            #angle += np.arctan2(x2 - x1, y2 - y1)


    if neg_cnt > pos_cnt:
        #nlines = neg_cnt
        #angle = neg_angle
        meanAngle = avgangle(cntDictNeg,valDictNeg,mainList,-1)
    else:
        #nlines = pos_cnt
        #angle = pos_angle
        meanAngle = avgangle(cntDictPos,valDictPos,mainList,+1)
        
    lin = plt.plot([x1,y1],[x2,y2])
    plt.setp(lin,color='b',linewidth=10)
    #plt.show()
    #lineimg = cv2.line(image,(86,434),(368,394),(255,0,255),5)
    cv2.imwrite('lineimg.jpg',lineimg)
    print '---------'
    #print angle
    #print nlines
    x  = meanAngle
    print x
    return x


def avgangle(cntDict, valDict, mainList,sign):
    # Store first entry in dict
    key, val = sorted(cntDict.iteritems(), key=lambda (k,v): (v,k), reverse=True)[0]
    # mean = sum / count
    mean = sign * float(valDict[key]) / cntDict[key]
    low = mean - 1
    high = mean + 1
    total = cnt = 0
    print sign
    print cntDict
    print valDict
    for i in range(len(mainList)):
        if (mainList[i-1] * sign) >= low and (mainList[i-1] * sign) <= high:
            total += mainList[i-1] * sign
            cnt += 1
        
    return sign * float(total) / cnt
    
def buildDict(angle):
    global valDictNeg, cntDictNeg, valDictPos, cntDictPos
    if (angle < 0.0):
        ceilVal = math.ceil(angle)
        
        if cntDictNeg.has_key(ceilVal):
            cntDictNeg[ceilVal] += 1
        else:
            cntDictNeg[ceilVal] = 1
        
        if valDictNeg.has_key(ceilVal):
            valDictNeg[ceilVal] += angle
        else:
            valDictNeg[ceilVal] = angle
            
            
    else:
        floorVal = math.floor(angle)
        
        if cntDictPos.has_key(floorVal):
            cntDictPos[floorVal] += 1
        else:
            cntDictPos[floorVal] = 1

        if valDictPos.has_key(floorVal):
            valDictPos[floorVal] += angle
        else:
            valDictPos[floorVal] = angle
    #print cntDictNeg
    return
                
def deskew(image, angle):
    imgorig = image.copy()
    #image = cv2.bitwise_not(image)
    non_zero_pixels = cv2.findNonZero(image)
    center, wh, theta = cv2.minAreaRect(non_zero_pixels)

    root_mat = cv2.getRotationMatrix2D(center, angle, 1)
    cols, rows = image.shape
    rotated = cv2.warpAffine(imgorig, root_mat, (cols, rows), flags=cv2.INTER_CUBIC)
    #rotated = imgorig
    #print rotated
    
    return cv2.getRectSubPix(rotated, (cols, rows), center)

#imgcopy = img.copy()
deskewed_image = deskew(img.copy(), compute_skew(img.copy()))
#deskewed_image = deskew(img.copy(), 7.86)
#new_image = np.hstack((img,deskewed_image))
cv2.imwrite('slant.jpg',deskewed_image)
#cv2.imwrite('slant.jpg',img2)

