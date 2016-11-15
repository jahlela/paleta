from PIL import Image

import math
import requests
import time

################### Helper Functions ###################

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

def is_too_dark(rgb):
      r, g, b = rgb

      luminance = ((r*0.299 + g*0.587 + b*0.114) / 256)

      return luminance < .15

################### Kmeans Analysis ###################

def get_kmeans(file_path=None, iterations=20):
    """ Takes in an image file_path and returns a list of RGB values that 
        represent the centroids of 5 k-mean clusters (dominant palette). 

        Optional: number of iterations """

    start_kmeans = time.time()


    if file_path is None:
        file_path = "static/img/demo/caterpillar.png"

    # Not elegant, but makes it not break
    elif file_path[0] == "/":
        file_path = file_path[1:]

    # Create image object
    image = Image.open(file_path).convert("RGB")
    width, height = image.size

    centroids = [(255,255,255), (0, 255, 255), (255,0, 255), (255,255,0), (200,200,200)]

    for _ in xrange(10):
        # List of tuples with the average of pixels that are most similar to that 
        # centroid and the count of those pixels. The count is non-zero to prevent
        # division by zero errors
        nearests = [((0,0,0),0.00001) for _ in xrange(len(centroids))]

        # For each pixel in the image (defined by width and height)
        for i in xrange(width/8):
            for j in xrange(height/8):
                # Use PIL's .getpixel() to find the RGB color at each pixel
                pixel = image.getpixel((8*i,8*j))

                if is_too_dark(pixel):
                    continue

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
    print '\n Kmeans time elapsed: ', (time.time() - start_kmeans)

    return centroids



