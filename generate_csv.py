# Generate CSV

from PIL import Image, ImageOps, ImageEnhance, ImageFilter, ImageChops
import os, logging, argparse, re
import cv2
import numpy as np

image_files=[]
parser = argparse.ArgumentParser(description='A program that creates lumens CSV file from the input jpg files.')
parser.add_argument("dir", help="input directory containing image files")
args = parser.parse_args()

#print(args.dir)
for root, dirs, files in os.walk(args.dir):
    os.chdir(root)
    for file in files:
        #MatchObj = re.search('(\d).jpg', file)
        MatchObj = re.search('(^crop_thinv_.*).jpg', file)
        if MatchObj:
            image_files.append(os.path.join(root, file))

if (len(image_files) == 0):
    logging.error('No input file find so cannot continue')
    exit()


def write_lumen_matrix(image_file, File):
    # Below code will open the file
    #image = Image.open('C:\\Users\\dt79774\\Documents\\5.jpg')
    print image_file
    #image = Image.open(image_file)
    image = cv2.imread(image_file, cv2.IMREAD_GRAYSCALE)
    
    # The below code will convert the data into black and white
    #image = image.convert('L')
    
    #Below code will enhance the images as required
    #enhanceContrast = ImageEnhance.Contrast(image)
    #image = enhanceContrast.enhance(6.0)
    
    # Below code will FILTER the images.
    #image = image.filter(ImageFilter.UnsharpMask(radius=3, percent=200, threshold=10))
    #image = image.filter(ImageFilter.MinFilter(3))
    #image = image.filter(ImageFilter.SMOOTH)

    #Below code will enhance the images as required
    #enhanceContrast = ImageEnhance.Contrast(image)
    #image = enhanceContrast.enhance(3.0)
    
   # Clear the corners of the image  
    image_width, image_height = image.shape
    #print ('image_width is {} and image_height is {}'.format(image_width, image_height))
    #image_pixel = image.load()
    #for height in range(image_height):
    #    for width in range(image_width):
    #        if ((width < 1 or width > (image_width - 1) or height < 1 or height > (image_height -1)) or image_pixel[width, height] < 100): 
    #            #if (image_pixel[width, height] < 120):
    #            #((width < 4 or width > (image_width - 4) or height < 4 or height > (image_height - 4)) and image_pixel[width, height]) < 30):
    #               image.putpixel((width, height), 0)

            
    # The below code will get the box which contains the non zero pixels
    #image_box = image.getbbox()
    
    # Below code will get the the cropped image as per the image_box
    #image = image.crop(image_box)
    
    # The below code will resize the code to desired size
    disired_size = (28, 28)
    #image = ImageOps.fit(image, disired_size, method=Image.ANTIALIAS, bleed=0.0, centering=(.5, .5))
    #image = image.resize(disired_size, Image.ANTIALIAS)

    image = cv2.resize(image, (28, 28)) 
    
    #Add dark border around the corner so the images match up to MNIST images
    #new_size = (36,36)
    #new_image = Image.new("L", new_size)
    #new_image.paste(image, (int((new_size[0] - disired_size[0])/2), int((new_size[1] - disired_size[1])/2)))
    #image = new_image.resize(disired_size, Image.ANTIALIAS)
    
    #Below code is used to save the images.
    (filepath, filename) = os.path.split(image_file)
    #cv2.imwrite('\\saved\\' +'abc_' + filename,image)
    cv2.imwrite(filepath + '\\saved\\' +'abc_' + filename,image)
    
    
    # Below code will create the excel to be imported to H2o code.
    image_pixel = image.copy()
    result_digit = re.search('(\d).jpg', image_file).group(1)
    lumen_string = result_digit + ','
    for width in range(disired_size[0]):
        for height in range(disired_size[1]):
            lumen_string += str(image_pixel[width, height]) + ','

    lumen_string += '\n'
    File.write(lumen_string)


with open ('lumens.csv', 'w') as F:
    for image_file in image_files:
        print image_file
        write_lumen_matrix(image_file, F)
