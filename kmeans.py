from PIL import Image
from colour import Color

import os.path
import math
import colorsys
import requests


def define_os_path():
    # Prepend os file path to image 
    os_path = os.path.dirname(os.path.abspath(__file__))
    return os_path



################### Image Analysis ###################

def get_pixels(URL=None, os_boolean=False):
    """ Takes a URL string and a boolean for whether the image is stored on the 
        local machine, and returns an Image object """

    if URL is None:
        URL = "static/img/demo/caterpillar.png"

    # Create image object
    image = Image.open(URL).convert("RGB")
    width, height = image.size

    all_pixels = []



    def distance(p1, p2):
        x1,y1,z1 = p1
        x2,y2,z2 = p2
        return (x1 - x2)**2 + (y1 - y2)**2 + (z1 - z2)**2

    def add(p1,p2):
        x1,y1,z1 = p1
        x2,y2,z2 = p2
        return (x1 + x2, y1 + y2, z1 + z2)

    def mult(p,s):
        return (s * p[0], s * p[1], s * p[2])

    centroids = [(255,255,255), (0, 255, 255), (255,0, 255), (255,255,0), (200,200,200)]

# c = centroid in all abbrvs
    counter = 1

    for _ in xrange(20):
        # print "\n \n Big Iteration", counter
        counter += 1

        # List of tuples with the average of pixels that are most similar to that 
        # centroid and the count of those pixels
        nearests = [((0,0,0),0.00001) for _ in xrange(len(centroids))]

        # For each pixel in the image (defined by width and height)
        for i in xrange(width/8):
            for j in xrange(height/8):
                # Use PIL's .getpixel() to find the RGB color at each pixel
                pixel = image.getpixel((8*i,8*j))

                # Default the min centroid index and min distance to 0 and infiniti
                min_cent_idx, min_dist = (0, float("inf"))
                for cent_idx in xrange(len(centroids)):
                    cent_dist = distance(centroids[cent_idx], pixel)
                    if cent_dist < min_dist:
                        min_cent_idx = cent_idx
                        min_dist = cent_dist

                (s,n) = nearests[min_cent_idx]
                nearests[min_cent_idx] = (add(pixel, s), n + 1)

        for cent_idx in xrange(len(centroids)):
            centroids[cent_idx] = mult(nearests[cent_idx][0], 1 / nearests[cent_idx][1])
        

        for idx in xrange(len(centroids)):
            centroids[idx] = (int(centroids[idx][0]), int(centroids[idx][1]), int(centroids[idx][2]))

    
    print '\n \t centroids', centroids


    return centroids

centroids = get_pixels() 



