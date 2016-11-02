
from PIL import Image
import os.path

################### Mise en place (Wash and prep) ###################

# Prepend os file path to image 
script_dir = os.path.dirname(os.path.abspath(__file__))
os_file_path = os.path.join(script_dir, 'img/jellyfish_color.jpg')

im = Image.open(os_file_path).convert('HSV')
w, h = im.size # Needed for .getcolors()

# Returns a list of unsorted tuples
# Format: (count, (H, S, V)) | Ex: (8034, (155, 63, 12))
get_colors = im.getcolors(w * h)

# Order colors from most to least common
get_colors.sort(reverse=True)

# Return most common colors
top_colors = get_colors[:30]

print '#############################'
print 'top_colors: ', top_colors


color_bins = {}


################### HELPER FUNCTIONS ###################

# Takes two integers, num and divisor. Rounds num down to nearest divisor (default 10)
# Ex. round_down(156) --> 150
# Ex. round_down(156, 5) --> 155
def round_down(num, divisor=10):
    return num - (num % divisor)