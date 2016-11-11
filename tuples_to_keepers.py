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