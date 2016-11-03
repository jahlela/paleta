
from PIL import Image
from colour import Color

import os.path
import math
import colorsys

import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(message)s')


################### HELPER FUNCTIONS ###################

# Takes two integers, num and divisor. Rounds num down to nearest divisor (default 10)
# Ex. round_down(156) --> 150
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
image = get_image_object('img/octopus.png')

def get_common_colors(image, num_colors=1000):
    """ Returns a list of tuples with most common colors and their pixel count. 

        Tuple format:  (count, (Hue, Saturation, Value))
        Tuple example: (8034, (155, 63, 12))

        Length of list is num_colors (optional, defaults to 1000)
     """
    
    # Width and height for .getcolors()
    w, h = image.size

    # Returns a list of unsorted tuples
    get_colors = image.getcolors(w * h)

    # Order colors from most to least common
    get_colors.sort(reverse=True)

    # Return most common colors
    common_colors = get_colors[:num_colors]

    # Return list of raw data tuples. Length of list is num_colors.
    return common_colors 


common_colors = get_common_colors(image) # add second argument for how many colors

print 'common_colors from real image, limit 100', common_colors[-100:]

# common_colors = [
#               (32212, (312, 0, 9)), (28376, (35, 0, 10)), (19168, (23, 47, 16)), 
#               (18000, (27, 51, 15)), (15429, (230, 42, 18)), (14265, (120, 0, 14)), 
#               (12679, (101, 0, 11)), (12460, (79, 45, 17)), (12452, (155, 40, 19)), 
#               (11642, (9, 0, 8)), (11571, (2, 0, 13)), (10700, (155, 54, 14)), 
#               (10261, (154, 78, 26)), (9488, (154, 75, 27)), (9328, (0, 0, 12)), 
#               (9030, (60, 69, 11)), (8945, (155, 38, 20)), (8812, (165, 81, 25)), 
#               (8606, (0, 0, 16)), (8034, (155, 63, 12)), (7986, (154, 72, 28)), 
#               (7855, (155, 58, 13)), (7756, (155, 36, 21)), (7406, (155, 34, 22)), 
#               (7313, (154, 65, 31)), (7136, (154, 85, 24)), (7066, (7, 0, 15)), 
#               (6899, (154, 68, 30)), (6827, (154, 70, 29)), (6777, (106, 34, 15))
#               ]

def create_color_bins():
    """ Create an empty list with 36 empty lists that will represent the 36 possible
        bins of color by hue. """

    color_bins = []

    # list of bins, one for each 10 degrees of hue
    for _ in xrange(36):
        color_bins.append([])

    return color_bins

# Create color_bins
color_bins = create_color_bins()


def fill_color_bins(color_bins, image_tuples):
    """ Takes a list of 36 empty lists and returns a list where each empty 
        list (bin) is now filled with tuples for colors belonging to that bin. """

    logging.debug('Length of color_bins should be 36 and is {:d}'.format(len(color_bins)))

    for raw_tuple in image_tuples:

        # Round hue down to the nearest 10
        adjusted_hue = round_down(raw_tuple[1][0])

        # Find the bucket index: 
        bucket_idx = int(math.floor(adjusted_hue/10))

        # Add the raw_tuple (format: (32212, (312, 0, 9)) ) to the appropriate bucket
        color_bins[bucket_idx].append(raw_tuple)

    # print '\n color_bins after adding. Total bins: ', len(color_bins), color_bins
    return color_bins


color_bins = fill_color_bins(color_bins, common_colors)


def tally_color_bins(color_bins):
    """ Takes in a list of lists of tuples with pixel count and HSV values for 36 bins.
        Returns a list of tuples with the pixel sum and most common color from each bin. """

    # Empty list that will hold each winning color 
    win_bins = []

    # Loop through each hue bin (which may be empty or have many tuples)
    for bin in color_bins:
        # If the bin is empty, skip it.
        if len(bin) == 0:
            pass
        # If the bin is not empty, add a new tuple to win_bins with the total pixel
        # count for the bin and the HSL value of the color
        else:
            # Find sum of all pixel counts in bin
            bin_sum = sum([tup[0] for tup in bin])
            # Find color with the highest pixel count in the bin. 
            # This should always be in the first tuple, since we already sorted 
            # them in get_common_colors
            hsv_color = bin[0][1]

            # Add each new tuple to win_bins
            win_bins.append((bin_sum, hsv_color))

    # Sort win_bins from most common to least common color
    win_bins.sort(reverse=True)

    return win_bins


top_colors = tally_color_bins(color_bins)

def get_display_colors(top_colors, color_limit):
    """ Takes a list of tuples of format (count, (Hue, Saturation, Value)) 
        and returns a list of hex colors. Length is color_limit. """

    print '\n top_colors', top_colors

    limited_colors = top_colors[:color_limit]
    display_colors = []

    # Convert each color from HSV --> RGB --> hex because strings are better
    for color_tuple in limited_colors:

        # Unpack HSV values from tuple
        hue, saturation, value = color_tuple[1]

        # Use colorsys to convert HSV --> RGB 
        # Must divide by a float, or colorsys will return (0,0,0)
        rgb_color = colorsys.hsv_to_rgb(hue/360.0, saturation/255.0, value/255.0)

        # Colour returns black and white as 'black' and 'white, not as a hex
        if rgb_color == (0,0,0):
            hex_color = '#000'
        elif rgb_color == (1,1,1):
            hex_color = '#FFF'
        else:
            # unpack to individual values for hex transformation
            red, green, blue = rgb_color
            # convert from RBG --> hex (default for Colour object)
            hex_color = Color(rgb=(red, green, blue)).get_hex()
    
        print 'hex_color', hex_color

        display_colors.append(hex_color)
            

    return display_colors


display_colors = get_display_colors(top_colors, 5)
print '\n display_colors', display_colors







