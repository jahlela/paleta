
from PIL import Image
from colour import Color

import os.path
import math
import colorsys


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
    get_colors = image.getcolors(w * h)

    # Order colors from most to least common
    get_colors.sort(reverse=True)

    # Return most common colors
    common_colors = get_colors[:num_colors]

    # Return list of raw data tuples. Length of list is num_colors.
    return common_colors 


common_colors = get_common_colors(image) # add second argument for how many colors


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
print 'top_colors', top_colors


def get_colors_for_display(top_colors, color_count_limit, color_type):
    """  """

    display_colors = top_colors[:color_count_limit-1]

    # I know, sucks to use two libraries for color conversions. 
    for color in display_colors:
        if color_type == 'rgb':
            # Use colorsys to convert HSV --> RGB
            color = colorsys.hsv_to_rgb(color)
        elif color_type  == 'hex':
            # Create Colour library object
            color = Color(color)
            # Use Colour to convert RGB --> hex
            color.hex





