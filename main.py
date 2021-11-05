import cv2
import numpy as np
import os
import math
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-size', type=int,help='Set size of image in image.', required=True)
parser.add_argument('-save_to', help='Name of the file it should save the output to.', required=True)
parser.add_argument('-image_to_match', help='Name of the file the images should match.', required=True)
parser.add_argument('-input_images', help='Folder of the input images.', required=True)


args = parser.parse_args()


image_to_match = cv2.imread(args.image_to_match)
images_dirs = os.listdir(args.input_images)
size_of_image = args.size


images = [cv2.imread(args.input_images +'/'+dir) for dir in images_dirs]

for image in images:
    height, width, channels = image.shape
    x = max(height, width)
    y = max(height, width)
    square= np.zeros((x,y,3), np.uint8)
    square[int((y-height)/2):int(y-(y-height)/2), int((x-width)/2):int(x-(x-width)/2)] = image

images = [cv2.resize(img, (size_of_image, size_of_image)) for img in images]
averages = [np.average(image) for image in images]
averages = [(np.average(image[:,:,0]),np.average(image[:,:,0]),np.average(image[:,:,0])) for image in images]

max_x = math.floor(image_to_match.shape[0]/size_of_image)*size_of_image
max_y = math.floor(image_to_match.shape[1]/size_of_image)*size_of_image
image_to_match = image_to_match[0:max_x, 0:max_y]

for x in range(round(max_x/size_of_image)):
    for y in range(round(max_y/size_of_image)):
        piece = image_to_match[x*size_of_image:(x+1)*size_of_image, y*size_of_image:(y+1)*size_of_image]
        piece_average = np.average(piece, axis=0)
        
        r_av = np.average(piece[:,:,0])
        g_av = np.average(piece[:,:,1])
        b_av = np.average(piece[:,:,2])
        
        best_image_index = 0
        closest = 1000000
        
        for i, average in enumerate(averages):
            difference = 0
            difference += abs(r_av - average[0])
            difference += abs(g_av - average[1])
            difference += abs(b_av - average[2])
        
            if difference < closest:
                closest = difference
                best_image_index = i
            
        image_to_match[x*size_of_image:(x+1)*size_of_image, y*size_of_image:(y+1)*size_of_image] = images[best_image_index]


cv2.imwrite(args.save_to, image_to_match)
