import PIL
from PIL import Image
from colour import Color
import os.path
import requests
import time

from kmeans import get_kmeans

################### HELPER FUNCTIONS ###################

def define_os_path():
    """ Fetch os file path """

    os_path = os.path.dirname(os.path.abspath(__file__))
    return os_path

################### Image Analysis ###################
def resize_and_save(local_file_name, input_height = 250.0):
    """ Takes an image file path and overwrites the image with a smaller version """

    # Open local image and get width and height
    image = Image.open(local_file_name)
    width, height = image.size

    # Define new height and width, keeping the ratio between them constant
    new_height = float(input_height)
    height_percent = (new_height / height)
    new_width = int(height_percent * width)

    # Resize image, preserving aspect ratio
    image = image.resize((new_width, int(new_height)), PIL.Image.ANTIALIAS)
    image.save(local_file_name, optimize=True, quality=95)
    image.close()


def resize_and_save(local_file_name):
    image = Image.open(local_file_name)
    width, height = image.size

    new_height = 250.0
    height_percent = (new_height / height)
    new_width = int(height_percent * width)

    image = image.resize((new_width, int(new_height)), PIL.Image.ANTIALIAS)
    image.save(local_file_name,optimize=True,quality=85)

def get_file_path(URL):
    """ Takes a web-hosted URL and returns the local file path of the image after
        performing a get request. """

    # Start timer for get request
    start_get = time.time()

    os_path = define_os_path()

    # Fake sites into thinking my app's request is coming from a browser
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) \
                    AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 \
                    Safari/537.36'}
    # Grab the image from a URL using fake browser headers
    image_response = requests.get(URL, headers=headers)
    # Show 
    print '\n Get request time elapsed: ', (time.time() - start_get)

    # Raise an error if the get request was unsuccessful

    if image_response.status_code is not 200:
        raise StandardError("Response code not 200. Try another image.")    

    # Create a hexidecimal hash of the image data string for a unique filename
    file_hash = hex(hash(image_response.content))
    print 'file_hash', file_hash

    # Sometimes there is a dash at the beginning -- not great for a file name
    # Replace the '-' with a 1 to maintain uniqueness
    if file_hash[0] == '-':
        local_file_name = '/static/img/photos/1' +  hex(hash(image_response.content))[2:] + '.png'
        file_hash_name = os_path + local_file_name
        print 'file_hash_name', file_hash_name
        
    # Create a filename as is
    else:
        local_file_name = '/static/img/photos/' + hex(hash(image_response.content))[1:] + '.png'
        file_hash_name = os_path + local_file_name
        print 'file_hash_name', file_hash_name

    # Write the image to local repository with the content hash as a name
    with open(file_hash_name,'wb') as new_image_file:
        new_image_file.write(image_response.content)

    # Pass the file_hash_name to be resized
    resize_and_save(file_hash_name)

    # return file_path
    return local_file_name


def get_image_and_palette(URL):
    """ Takes in a string URL of an image and returns a list of hex 
        strings with the image palette. """

    # Fail elegantly
    try:
        file_path = get_file_path(URL)
    except: 
        raise StandardError("File not valid. Try another image.")

    # Perform kmeans distribution analysis on the local file
    kmeans_list = get_kmeans(file_path)

    palette = []

    # Convert each color from RGB --> hex because strings are better
    for rgb_color in kmeans_list:

        # unpack to individual values for hex transformation
        red, green, blue = rgb_color

        # Create Colour object and convert from RBG --> hex
        hex_color = Color(rgb=(red/256.00, green/256.00, blue/256.00)).get_hex()

        # Add each hex color to final list
        palette.append(hex_color)

    return [file_path, palette]









