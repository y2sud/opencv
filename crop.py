#Crop the image containing all digits into individual images/digits

import os, sys
import cv2
import numpy as np
from matplotlib import pyplot as plt
import math
from PIL import Image, ImageChops, ImageOps

def remove_stray_dots(im, area):
    se1 = cv2.getStructuringElement(cv2.MORPH_RECT, area)
    mask = cv2.morphologyEx(im, cv2.MORPH_OPEN, se1)
    mask = np.dstack([mask]) / 255
    out = img * mask
    return (out)

def trim(im):
    bg = Image.new(im.mode, im.size, im.getpixel((0,0)))
    diff = ImageChops.difference(im, bg)
    diff = ImageChops.add(diff, diff, 2.0, -100)
    bbox = diff.getbbox()
    if bbox:
        return(bbox)

def normalize_size(im):
    bbox = im.getbbox()
    new_x2 = 700
    new_y2 = int((new_x2 * bbox[3])/bbox[2])
    new_im = im.resize((new_x2, new_y2), Image.LANCZOS)
    return(new_im)

def is_vertical_line(x, y, image_pixel):
    temp_line_lenght = 0
    for temp_y in range(y,  y + 20):
        #print ('image pixel [{}, {}] = {}'.format(x, temp_y, image_pixel[x, temp_y]))
        if(image_pixel[x, temp_y] < 200):
            temp_line_lenght += 1
            
    print ('line lenght [{}, {}] = {}'.format(x, y, temp_line_lenght))      
    if (temp_line_lenght > 14):
        print'line length : {}'.format(temp_line_lenght)
        return True
    else:
        return False

def get_batch_number_images(image):
    im = image.convert('L')
    image_pixel = im.load()
    Total_lines_expected = 3
    expected_lines_found = 0
    total_lines = 0
    image_width, image_height = im.size
    print ('image width : {}, image height : {}'.format(image_width, image_height))
    line_length = 0
    height_scanned = 0
    expected_line_length = 400
    height = 120
    while (height < image_height):
        print('total_lines : {}, line_length : {}, height_scanned : {}'.format(total_lines, line_length, height_scanned))
        height_scanned = height
        line_length = 0
        if (total_lines ==  Total_lines_expected):
            print('we are breaking as maximum lines reached')
            expected_lines_found = 1
            break
                  
        for width in range(90 , image_width - 50):
            #print ('image pixel [{}, {}] = {}'.format(width, height, image_pixel[width, height]))
            if (image_pixel[width, height] < 180):
                line_length += 1

            if (line_length > expected_line_length):
                total_lines +=1
                print('line lenght has crossed its limit so breaking up')
                height += 5 #this is to make sure that no line counted multiple times
                break

        height += 1
        #print height
                
    if (not expected_lines_found):
        return None
    
    #Below code is to get the box location after the third line
    bbox_x1, bbox_y1, bbox_x2, bbox_y2 = 0, 0 ,0 , 0
    bbox_x1_y1_set, bbox_x2_y2_set = 0, 0
    short_line_length = 0
    temp_x = 200
    print ('height_scanned {}'.format(height_scanned))
    height = height_scanned + 2
    while (height < height + 50):
        print ('height: {}, line_length : {}'.format(height, short_line_length))
        short_line_length = 0
        for width in range(200 , image_width - 250):
            #print ('image pixel [{}, {}] = {}'.format(width, height, image_pixel[width, height]))
            if (image_pixel[width, height] < 200):
                short_line_length += 1
                if (short_line_length > 180 and not bbox_x1_y1_set):
                #if (short_line_length > 180 and (not bbox_x1_y1_set) or (bbox_x1_y1_set and (height - bbox_y1) == 1)):
                    # Go vertically down from our temprory position verify if our assumption is correct. Check for three consequtive lines
                    for x in range(temp_x, temp_x + 100):
                        print ('Checking line lenght for [{}, {}]'.format(x, height))
                        if (is_vertical_line(x, height, image_pixel)):
                            bbox_x1 = x
                            bbox_y1 = height
                            height += 25
                            bbox_x1_y1_set = 1
                            print 'bbox set, bbox_x1 : {}, bbox_y1 : {}'.format(bbox_x1, bbox_y1)
                            short_line_length = 0
                            break
                        if (bbox_x1 != 0):
                            break
                    else:
                        print('FATAL : Not able to find bbox')
                        sys.exit(1)
                else:
                    if (short_line_length > 180 and bbox_x1_y1_set):
                        #bbox_x2 = width
                        bbox_y2 = height
                        bbox_x2_y2_set = 1
                        print 'bbox set, bbox_y2 : {}'.format(bbox_y2)
                        #print 'inside else : bbox_x2_y2_set : {}'.format(bbox_x2_y2_set)
                        break
            if(bbox_x2_y2_set):
                break
        #print 'outside loop : bbox_x2_y2_set : {}'.format(bbox_x2_y2_set)
        if(bbox_x2_y2_set):
            break
        height += 1
        
    # Since we have got x1, y1 and y2 .. we can start looking for different numbers bbox
    #bbox = {}
    number_image_count = 0 # This will keep check the number of image as we can have only 6 numbers
    temp_x = bbox_x1 + 30 # since we have already identified the first x, next search will start only after increasing by 20 pixels as the box lenght will minimum be 20
    previous_x = bbox_x1 # Keep check of last x found as the ending x of last image is the starting x1 of new image 
    while (temp_x < temp_x + 250): # the line lenght will not be more than 250 hence the check
        print('checkin for location x : {}, y : {}'.format({temp_x}, {bbox_y1}))
        if (is_vertical_line(temp_x, bbox_y1, image_pixel)):
            bbox = [previous_x + 2, bbox_y1 + 2, temp_x + 2, bbox_y2 + 2]
            new_image =  image.crop(bbox)
            new_image.save('temp.jpg')
            num_img = cv2.imread('temp.jpg')
            ret, num_img_bw = cv2.threshold(num_img,180,255,cv2.THRESH_BINARY)
            se1 = cv2.getStructuringElement(cv2.MORPH_RECT, (1,1))
            mask = cv2.morphologyEx(num_img_bw, cv2.MORPH_OPEN, se1)
            mask = np.dstack([mask]) / 255
            out = num_img_bw * mask

            #modified_img_bw = remove_stray_dots(num_img_bw, (10,10))
            cv2.imwrite('temp' + str(number_image_count) + '.jpg', out)
            im_ref = Image.open('temp' + str(number_image_count) + '.jpg')
            new_bbox = trim(im_ref)
            #print bbox
            new_image.crop([new_bbox[0] + 3,new_bbox[1] +3, new_bbox[2] - 3,new_bbox[3] - 3]).save('number_' + str(number_image_count) + '.jpg')
            previous_x = temp_x + 1
            print 'privious_x : {}'.format(previous_x)
            number_image_count += 1
            temp_x += 30

        if (number_image_count == 6):
            break
        temp_x += 1
    #return ((bbox_x1, bbox_y1, bbox_x2, bbox_y2))
    #'''

os.chdir('1 page')
img = cv2.imread('slant.jpg')
#img = cv2.imread('temp.jpg')
# make ithe image black & white
ret, img_bw = cv2.threshold(img,127,255,cv2.THRESH_BINARY)

modified_image = remove_stray_dots(img_bw, (10,10))
cv2.imwrite('output.jpg', modified_image)

# Below section deals with image module.
im_ref = Image.open('output.jpg')
trim_bbox = trim(im_ref)
im_orig = Image.open('slant.jpg')
cropped_im = im_orig.crop(trim_bbox)
normalized_im = normalize_size(cropped_im)
normalized_im.save('cropped.jpg')
get_batch_number_images(normalized_im)

