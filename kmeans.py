from PIL import Image

import random
import math
import requests
import time

################### Helper Functions ###################

def distance(point1, point2):
    """ Find Euclidean distance between two points in 3D space """
    x1,y1,z1 = point1
    x2,y2,z2 = point2
    return (x1 - x2)**2 + (y1 - y2)**2 + (z1 - z2)**2

def add(point1,point2):
    """ Add two 3D points, element-wise """
    x1,y1,z1 = point1
    x2,y2,z2 = point2
    return (x1 + x2, y1 + y2, z1 + z2)

def mult(point_sums, point_count):
    """ Note: with kmeans usage, point-count will be 1/count """
    x, y, z = point_sums
    return (x * point_count, y * point_count, z * point_count)

def is_too_dark(rgb, too_low=.05):
    """ Takes an RGB value and returns True if the luminance is too low """
    r, g, b = rgb
    luminance = ((r*0.299 + g*0.587 + b*0.114) / 256.0)
    return luminance < too_low

def get_random_rgb():
    rgb_tuple = []

    for _ in xrange(3):
        rgb_tuple.append(random.randint(0,255))

    return tuple(rgb_tuple)

def nearest_is_empty(nearests):
    """ Checks for nearests with no members and tries another color """
    for nearest in nearests:
        if nearest[0] is (0,0,0):
            nearest[0] = get_random_rgb()

################### Kmeans Analysis ###################

def get_kmeans(file_path=None, iterations=20):
    """ Takes in an image file_path and returns a list of RGB values that 
        represent the centroids of 5 k-mean clusters (dominant palette). 

        Optional: number of iterations """

    start_kmeans = time.time()

    if file_path is None:
        file_path = "static/img/demo/caterpillar.png"

    # Not elegant, but makes it not break
    # Please do not delete without testing!
    elif file_path[0] == "/":
        file_path = file_path[1:]

    # Create image object
    image = Image.open(file_path).convert("RGB")
    width, height = image.size

    centroids = [(255,255,255), (0, 255, 255), (255,0, 255), (255,255,0), (200,200,200)]

    for count in xrange(iterations):

        # List of tuples with the average of pixels that are most similar to that 
        # centroid and the count of those pixels. The count is non-zero to prevent
        # division by zero errors
        nearests = [((0,0,0),0.1) for _ in xrange(len(centroids))]

        # For each pixel in the image (defined by width and height)
        for j in xrange(height/2):        
            for i in xrange(width/2):
                # Use PIL's .getpixel() to find the RGB color at each pixel
                pixel = image.getpixel((2*i,2*j))

                # Skip this pixel if it's luminance is too low
                if is_too_dark(pixel):
                    continue

                # Default the min centroid index and min distance to 0 and infiniti
                min_cent_idx, min_dist = (0, float("inf"))
                for cent_idx in xrange(len(centroids)):
                    cent_dist = distance(centroids[cent_idx], pixel)
                    if cent_dist < min_dist:
                        min_cent_idx = cent_idx
                        min_dist = cent_dist

                (s,point_count) = nearests[min_cent_idx]
                nearests[min_cent_idx] = (add(pixel, s), point_count + 1)
        
        for cent_idx in xrange(len(centroids)):
            
            point_sums = nearests[cent_idx][0]
            point_count = 1 / nearests[cent_idx][1]

            # Reset each of the centroids to the average of all colors closest
            # to that centroid
            point_average = mult(point_sums, point_count)
            centroids[cent_idx] =  point_average

        for idx in xrange(len(centroids)):
            centroids[idx] = (int(centroids[idx][0]), int(centroids[idx][1]), int(centroids[idx][2]))

    print '\n Kmeans time elapsed: ', (time.time() - start_kmeans)
    return centroids



