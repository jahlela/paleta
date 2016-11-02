
from PIL import Image
from colour import Color

import os.path
import math


################### HELPER FUNCTIONS ###################

# Takes two integers, num and divisor. Rounds num down to nearest divisor (default 10)
# Ex. round_down(156) --> 150
# Ex. round_down(156, 5) --> 155
def round_down(num, divisor=10):
    """ Round down to nearest divisor (default 10) """
    return num - (num % divisor)


################### Image Analysis ###################

def get_image_object(file_path):
    """ Creates Image object with HSV color profile """

    # Prepend os file path to image (helps prevent )
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os_file_path = os.path.join(script_dir, file_path)

    # Create image object using HSV 
    image = Image.open(os_file_path).convert('HSV')

    return image

# Set test image
image = get_image_object('img/sunset.jpg')

def get_common_colors(image, num_colors=1000):
    """ Returns a list of tuples with most common colors and their pixel count. 

        Tuple format:  (count, (Hue, Saturation, Value))
        Tuple example: (8034, (155, 63, 12))

        Length of list is num_colors (optional, defaults to 1000)
     """
    
    # Width and height for .getcolors()
    w, h = image.size

    # Returns a list of unsorted tuples
    # http://pillow.readthedocs.io/en/3.4.x/reference/Image.html?highlight=histogram#PIL.Image.Image.getcolors
    get_colors = image.getcolors(w * h)

    # Order colors from most to least common
    get_colors.sort(reverse=True)

    # Return most common colors
    common_colors = get_colors[:num_colors]

    # Return list of raw data tuples. Length of list is num_colors.
    return common_colors 


common_colors = get_common_colors(image) # add second argument for how many colors


# Remove this once there is real data
demo_colors = [
              (32212, (312, 0, 9)), (28376, (35, 0, 10)), (19168, (23, 47, 16)), 
              (18000, (27, 51, 15)), (15429, (230, 42, 18)), (14265, (120, 0, 14)), 
              (12679, (101, 0, 11)), (12460, (79, 45, 17)), (12452, (155, 40, 19)), 
              (11642, (9, 0, 8)), (11571, (2, 0, 13)), (10700, (155, 54, 14)), 
              (10261, (154, 78, 26)), (9488, (154, 75, 27)), (9328, (0, 0, 12)), 
              (9030, (60, 69, 11)), (8945, (155, 38, 20)), (8812, (165, 81, 25)), 
              (8606, (0, 0, 16)), (8034, (155, 63, 12)), (7986, (154, 72, 28)), 
              (7855, (155, 58, 13)), (7756, (155, 36, 21)), (7406, (155, 34, 22)), 
              (7313, (154, 65, 31)), (7136, (154, 85, 24)), (7066, (7, 0, 15)), 
              (6899, (154, 68, 30)), (6827, (154, 70, 29)), (6777, (106, 34, 15))
              ]


def create_color_bins():
    """ """
    color_bins = []

    # list of bins, one for each 10 degrees in Hue
    for _ in xrange(36):
        color_bins.append([])

    return color_bins

color_bins = create_color_bins()


def fill_color_bins(color_bins, image_tuples):
    """ """
    print 'empty color_bins', color_bins

    print 'image_tuples: ', len(image_tuples), image_tuples
    
    for raw_tuple in image_tuples:
        print
        print 'raw_tuple', raw_tuple

        # Round hue down to the nearest 10
        adjusted_hue = round_down(raw_tuple[1][0])
        print 'adjusted_hue', adjusted_hue

        # Find the bucket index: 
        bucket_idx = int(math.floor(adjusted_hue/10))
        print 'bucket_idx', bucket_idx

        # Add the raw_tuple (format: (32212, (312, 0, 9)) ) to the appropriate bucket
        color_bins[bucket_idx].append(raw_tuple)
        print 'color_bins[bucket_idx]', color_bins[bucket_idx]



    # print '\n color_bins after adding. Total bins: ', len(color_bins), color_bins
    return color_bins



color_bins = fill_color_bins(color_bins, demo_colors)
print '\n color_bins[0]', color_bins[0]


# def tally_color_bins(color_bins):
#     """ """

#     win_bins = []

#     for bin in color_bins:
#         bin_sum = sum([tup[0] for tup in bin])

#         win_bins.append((bin_sum, bin[1]))

#     print '\n win_bins', win_bins[0]
#     return win_bins


# tally_color_bins(color_bins)



# [
#     # Implied index based on hue
#     [(84, (15, 63, 12)), (34, (12, 63, 12)), (4, (18, 43, 12))]

# ]

# [
#     # H is 0-9
#     (total_pixels, [])
#     (0, [tuple1, tuple2, tuple3])
#     # tuples with total_pixels and list of raw data tuples 
#     (8042, [(8034, (5, 63, 12)), (8, (1, 63, 12))]),

#     # Or, leave off total_pixels and calculate on the fly
#     [(84, (15, 63, 12)), (34, (12, 63, 12)), (4, (18, 43, 12))],
    
# ]









