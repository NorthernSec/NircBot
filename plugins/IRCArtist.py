from urllib  import request
from PIL     import Image, ImageChops

from colormath.color_objects     import LabColor, sRGBColor
from colormath.color_conversions import convert_color

import logging

logger = logging.getLogger('colormath')
logger.setLevel(logging.INFO)
logger = logging.getLogger('PIL')
logger.setLevel(logging.INFO)

import numpy as np
import sys, math, io, time


ircColors = {(211, 215, 207): 0,
             ( 46,  52,  54): 1,
             ( 52, 101, 164): 2,
             ( 78, 154,   6): 3,
             (204,   0,   0): 4,
             (143,  57,   2): 5,
             ( 92,  53, 102): 6,
             (206,  92,   0): 7,
             (196, 160,   0): 8,
             (115, 210,  22): 9,
             ( 17, 168, 121): 10,
             ( 88, 161, 157): 11,
             ( 87, 121, 158): 12,
             (160,  67, 101): 13,
             ( 85,  87,  83): 14,
             (136, 137, 133): 15}
colors = list(ircColors.keys())


class IRCArtist:
    name     = "IRCArtist"
    commands = ['art']


    def command(self, bot=None, command=None, arguments=None, nick=None,
                      channel=None, ident=None, host=None, **args):
        if not (bot and command and arguments and channel):
            return
        if command == 'art':
            try:
                image = self.get_image(arguments)
                image = self.crop(image)
                image = self.resize_if_needed(image)
                if image:
                    for line in self.generate_image(image):
                        bot.say(channel, line)
                    return
                bot.say(channel, "Could not fetch image")
            except Exception as e:
                print(e)
                bot.say(channel, "Invalid image")

    def get_image(self, link):
        data = request.urlopen(link).read()
        if not data:
            return None
        stream = io.BytesIO(data)
        img = Image.open(stream).convert('P').convert('RGBA')
        return img

    def resize_if_needed(self, image, max_size=32):
        width, height = image.size
        ratio = min(max_size/width, max_size/height)
        new_width  = int(width*ratio)
        new_height = int(height*ratio)
        image = image.resize((new_width, new_height))
        return image

    def crop(self, image):
        bg = Image.new(image.mode, image.size, image.getpixel((0,0)))
        diff = ImageChops.difference(image, bg)
        diff = ImageChops.add(diff, diff, 2.0, -100)
        bbox = diff.getbbox()
        if bbox:
            return image.crop(bbox)

    def distance(self, rgb, c1, c2):
        if rgb:
            (r1,g1,b1) = (c1[0], c1[1], c1[2])
            (r2,g2,b2) = (c2[0], c2[1], c2[2])
        else:
            rgb1 = sRGBColor(c1[0], c1[1], c1[2])
            rgb2 = sRGBColor(c2[0], c2[1], c2[2])
            lab1 = convert_color(rgb1, LabColor)
            lab2 = convert_color(rgb2, LabColor)
            (r1,g1,b1) = lab1.lab_l, lab1.lab_a, lab1.lab_b
            (r2,g2,b2) = lab2.lab_l, lab2.lab_a, lab2.lab_b

        return math.sqrt((r1 - r2)**2 + (g1 - g2) ** 2 + (b1 - b2) **2)

    def generate_image(self, image, rgb=False):
        arr = np.array(np.asarray(image).astype('float'))
        lines = []
        for line in arr:
            row = ""
            for pixel in line:
                if pixel[3] == 0:
                    row += "\003  " # \003 to close any potential open color tag
                else:
                    closest_colors = sorted(colors, key=lambda color: self.distance(rgb, color, pixel))
                    closest_color = closest_colors[0]
                    row += "\003{0},{0}  ".format(ircColors[closest_color])
            yield row
