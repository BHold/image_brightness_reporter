import argparse
import math
import os
from PIL import Image, ImageStat

def get_perceived_brightness(image_file):
    """
    Returns an integer value representing the perceived brightness of an image.
    This takes into account that human eyes are sensitive to light in the order
    of green > red > blue.
    """
    with Image.open(image_file) as image:
        image_stat = ImageStat.Stat(image)
        r = image_stat.mean[0]
        g = image_stat.mean[1]
        b = image_stat.mean[2]
        return math.sqrt(0.241*(r**2) + 0.691*(g**2) + 0.068*(b**2))

def print_output(filename):
    try:
        brightness = get_perceived_brightness(filename)
    except Exception as err:
        print("Skipping unreadable image {0}: {1}".format(filename, err))
        return
    print("{0:3.2f}:  {1}\n".format(brightness, filename))

def output_brightness(path):
    if os.path.isdir(path):
        files = [f for f in os.listdir(path) if
            os.path.isfile(os.path.join(path, f))]
        for f in files:
            print_output(os.path.join(path, f))
    else:
        print_output(path)

parser = argparse.ArgumentParser()
parser.add_argument("path", help="File path to the image or folder of images.")
args = parser.parse_args()
output_brightness(args.path)
