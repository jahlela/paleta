
from PIL import Image
import os.path
import math

################### HELPER FUNCTIONS ###################

# Takes two integers, num and divisor. Rounds num down to nearest divisor (default 10)
# Ex. round_down(156) --> 150
# Ex. round_down(156, 5) --> 155
def round_down(num, divisor=10):
    return num - (num % divisor)


def get_bucket_index(hue):
    return int(math.floor(hue/10))



################### Image Analysis ###################

def get_image_object(file_path):

    # Prepend os file path to image 
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os_file_path = os.path.join(script_dir, file_path)

    image = Image.open(os_file_path).convert('HSV')

    return image

# Set test image
image = get_image_object('img/sunset.jpg')


# default to 100 most common colors
def get_top_colors_raw(image, num_colors=1000):
    
    # Get width and height for .getcolors()
    w, h = image.size

    # Returns a list of unsorted tuples
    # Format: (count, (H, S, V)) | Ex: (8034, (155, 63, 12))
    get_colors = image.getcolors(w * h)

    # Order colors from most to least common
    get_colors.sort(reverse=True)

    # Return most common colors
    top_colors = get_colors[:num_colors]

    return top_colors # List of raw data tuples. Length of list is num_colors.


top_colors = get_top_colors_raw(image)

print '#############################'
# print 'top_colors: ', len(top_colors), top_colors


# Get raw data

# Loop through raw --> array of lists for each bucket_index w/ list of tuples, no total

# Loop through that: for each index, sort tuples and calc total 
# Create new data struct that is a list of tuples with total_pixels and list of raw data tuples 

# Sort list of tuples by total_pixels and 5 top buckets

# Loop through each bucket and find most common value in that bucket 


def create_color_bins():
    color_bins = []

    for _ in xrange(36):
        color_bins.append([])

    return color_bins


color_bins = create_color_bins()

# This will become top_colors with real data
image_tuples = [(32212, (0, 0, 9)), (28376, (0, 0, 10)), (19168, (155, 47, 16)), (18000, (155, 51, 15)), (15429, (155, 42, 18)), (14265, (0, 0, 14)), (12679, (0, 0, 11)), (12460, (155, 45, 17)), (12452, (155, 40, 19)), (11642, (0, 0, 8)), (11571, (0, 0, 13)), (10700, (155, 54, 14)), (10261, (154, 78, 26)), (9488, (154, 75, 27)), (9328, (0, 0, 12)), (9030, (155, 69, 11)), (8945, (155, 38, 20)), (8812, (154, 81, 25)), (8606, (0, 0, 16)), (8034, (155, 63, 12)), (7986, (154, 72, 28)), (7855, (155, 58, 13)), (7756, (155, 36, 21)), (7406, (155, 34, 22)), (7313, (154, 65, 31)), (7136, (154, 85, 24)), (7066, (0, 0, 15)), (6899, (154, 68, 30)), (6827, (154, 70, 29)), (6777, (106, 34, 15))]



def fill_color_bins(color_bins, image_tuples):
    
    for raw_tuple in image_tuples:
        print 'raw_tuple', raw_tuple
        adjusted_hue = round_down(raw_tuple[1][0])
        print 'adjusted_hue', adjusted_hue

##############################################
# THIS IS WEIRD
        idx = get_bucket_index(adjusted_hue)
        print "idx", idx

        color_bins.append(raw_tuple)

    return color_bins



answer = fill_color_bins(color_bins, image_tuples)

print answer

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









