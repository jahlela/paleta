from PIL import Image
from colour import Color

import os.path
import math
import colorsys
import requests

import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(message)s')


################### HELPER FUNCTIONS ###################

def round_down(num, divisor=10):
    """ Rounds integer down to nearest divisor (default 10) """
    return num - (num % divisor)

def define_os_path():
    # Prepend os file path to image 
    os_path = os.path.dirname(os.path.abspath(__file__))
    return os_path



################### Image Analysis ###################

def get_image_object(URL, os_boolean):
    """ Takes a URL string and a boolean for whether the image is stored on the 
        local machine, and returns an Image object with HSV color profile. """

    if os_boolean:
        os_path = define_os_path()
        os_file_path = os.path.join(os_path, URL)
        # Create image object using HSV 
        image = Image.open(os_file_path).convert('HSV')
    else:
        # Create image object using HSV 
        image = Image.open(URL).convert('HSV')
    
    return image



def get_common_colors(image, num_colors=1000):
    """ Takes an Image object and an integer for how many colors to sample, and 
        Returns a list of tuples with most common colors and their pixel count. 

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


    total_pixels = 0
    for tuple in get_colors:
        total_pixels += tuple[0]

    # Return most common colors
    common_colors = get_colors[:num_colors]

    # Return list of raw data tuples. Length of list is num_colors.
    return [common_colors, total_pixels]




def create_color_bins():
    """ Create an empty list with 36 empty lists that will represent the 36 possible
        bins of color by hue. """

    color_bins = []

    # list of bins, one for each 10 degrees of hue
    for _ in xrange(36):
        color_bins.append([])

    return color_bins



def fill_color_bins(color_bins, image_tuples):
    """ Takes a list of 36 empty lists and returns a list where each empty 
        list (bin) is now filled with tuples for colors belonging to that bin. """

    logging.debug('Length of color_bins should be 36 and is {:d}'.format(len(color_bins)))

    for raw_tuple in image_tuples:

        # Round hue down to the nearest 10
        adjusted_hue = round_down(raw_tuple[1][0])

        # Find the bucket index: 
        bucket_idx = int(math.floor(adjusted_hue/10))

        # Add the raw_tuple of format: (32212, (312, 0, 9)) to its bucket
        color_bins[bucket_idx].append(raw_tuple)

    return color_bins



def tally_color_bins(color_bins):
    """ Takes in a list of lists of tuples with pixel count and HSV values for 36 bins.
        Returns a list of tuples with the pixel sum and most common color from each bin. """

    # Empty list that will hold the winning color from each bin
    top_bin_colors = []

    # Loop through each hue bin (which may be empty or have many tuples)
    for bin in color_bins:
        # If the bin is empty, skip it.
        if len(bin) == 0:
            pass
        # If the bin is not empty, add a new tuple to top_bin_colors with the total pixel
        # count for the bin and the HSL value of the color
        else:
            # Find sum of all pixel counts in bin
            bin_sum = sum([tup[0] for tup in bin])
            # Find color with the highest pixel count in the bin. 
            # This should always be in the first tuple, since we already sorted 
            # them in get_common_colors
            hsv_color = bin[0][1]

            # Add each new tuple to top_bin_colors
            top_bin_colors.append((bin_sum, hsv_color))

    # Sort win_bins from most common to least common color
    top_bin_colors.sort(reverse=True)

    return top_bin_colors




def get_display_colors(top_bin_colors, color_limit, total_pixels):
    """ Takes a list of tuples of format (count, (Hue, Saturation, Value)) 
        and returns a list of hex colors. Length is color_limit. """

    # pick the n most common colors, defined by user with color_limit
    limited_colors = top_bin_colors[:color_limit]

    # This will be the final output of hex values for dominant colors
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
            hex_color = '#000000'
        elif rgb_color == (1,1,1):
            hex_color = '#FFF000'
        else:
            # unpack to individual values for hex transformation
            red, green, blue = rgb_color

            # Create Colour object and convert from RBG --> hex
            hex_color = Color(rgb=(red, green, blue)).get_hex()


        # Get pixel count from individual color
        pixel_count = color_tuple[0]

        # Here is the percent of each color, in case anyone is interested later
        percent_color = int((float(pixel_count)/total_pixels)*100)
        
        # Add each hex color to final list
        display_colors.append(hex_color)
            
    # These will go on the site!
    return display_colors



def get_palette(URL, os_boolean, sample_limit, palette_limit=5):
    """ Takes in a string URL of an image, a boolean for whether the image is 
        stored on the local machine, two integers for limits on sample size and 
        palette size, and returns a list of hex strings with the image palette. """

    # Set test image
    image = get_image_object(URL, os_boolean)
    # image = get_image_object('static/img/caterpillar.png')

    # Add optional second argument for how many colors to sample 
    # (500+ is good, though more than 2000 sees little change in output)
    common_colors, total_pixels = get_common_colors(image, sample_limit)

    # Create 36 color_bins (one for each 10 degrees of hue)
    color_bins = create_color_bins()

    # Fill each of the 36 color_bins with the raw tuples 
    color_bins_filled = fill_color_bins(color_bins, common_colors)

    # Get top color from each bin in HSV format
    top_bin_colors = tally_color_bins(color_bins_filled)
    print top_bin_colors

    # Get final palette in hex with user-defined limit
    palette = get_display_colors(top_bin_colors, palette_limit, total_pixels)
    print 'palette', palette 

    return palette



def hash_photo(URL):

    os_path = define_os_path()

    # Grab the image from a URL
    image_response = requests.get(URL)    

    # Create a hexidecimal hash of the image data string for a unique filename
    file_hash = hex(hash(image_response.content))

    # Sometimes there is a dash at the beginning -- not great for a file name
    # Replace the '-' with a 1 to maintain uniqueness
    if file_hash[0] == '-':
        local_file_name = '/static/img/photos/1' +  hex(hash(image_response.content))[2:] + '.png'
        file_hash_name = os_path + local_file_name
        
    # Create a filename as is
    else:
        local_file_name = '/static/img/photos/' + hex(hash(image_response.content))[1:] + '.png'
        file_hash_name = os_path + local_file_name

    # Write the image to local repository with the content hash as a name
    with open(file_hash_name,'wb') as new_image_file:
        new_image_file.write(image_response.content)

    # Get a palette, ex. "#4ac84c,#c2d2ce,#3e3a50,#674f4f,#c0cfca"
    palette = get_palette(file_hash_name, False, 3000)
    palette = str(','.join(palette))

    # This is slightly different than the /profile way, but it works.
    return [local_file_name, palette]


