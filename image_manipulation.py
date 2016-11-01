
from PIL import Image
import os.path

script_dir = os.path.dirname(os.path.abspath(__file__))
os_file_path = os.path.join(script_dir, 'img/jellyfish_color.jpg')

im = Image.open(os_file_path)
w, h = im.size


print '#############################'
get_colors = im.getcolors(w * h)
get_colors.sort(reverse=True)
top_colors = get_colors[:10]

print 'top_colors', top_colors
