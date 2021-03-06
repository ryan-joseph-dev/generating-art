#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from itertools import product
from PIL import Image, ImageDraw
import random
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


def save_animated_gif(filename, images, durations):
    """
    Save images as frames of an animated GIF.  Durations should specify the
    milliseconds to display each frame, and should be of the same length as
    images.
    """
    first_image, *other_images = images
    backwards_images = other_images[::-1] # reversing using list slicing
    all_images = other_images + backwards_images + [first_image]
    durations = durations + durations
    first_image.save(filename, save_all=True, append_images=all_images, duration=durations, loop=0)

def punch_hole(draw, x, y, section_size, hole_color):
    """
    For a square with a corner at (x, y) and sides of length section_size,
    divide it into 9 tiles, and fill the center tile with hole_color.
    """
    corner = (x + section_size // 3, y + section_size // 3)
    # -1 necessary due to https://github.com/python-pillow/Pillow/issues/3597
    opposite_corner = (x + section_size * 2//3 - 1, y + section_size * 2//3 - 1)
    draw.rectangle((corner, opposite_corner), fill=hole_color)

def make_carpets(n, carpet_color, hole_color):
    """
    Generate n PIL Images, each of Sierpiński's carpet with increasing levels
    of detail.
    """
    image_size = 3**n
    logger.info("drawingin initial square")
    carpet = Image.new("RGBA", (image_size, image_size), carpet_color)
    yield carpet
    for section_size in (3**i for i in range(n, 1, -1)):
        logger.info(f"drawing inner square of size: {section_size}")
        carpet = carpet.copy()
        draw = ImageDraw.Draw(carpet)
        for x, y in product(range(0, image_size, section_size), repeat=2):
            punch_hole(draw, x, y, section_size, hole_color)
        yield carpet
        # to save each intermediate image, unccoment the line below
        # carpet.save(f"output/carpet{section_size}.png")
        
def random_color():
    """
    Generate a random hex color.
    """
    r = lambda: random.randint(0,255)
    return('#%02X%02X%02X' % (r(),r(),r()))

def main():
    N = 6
    
    carpet_color = random_color()
    hole_color = random_color()

    carpets = make_carpets(N, carpet_color=carpet_color, hole_color=hole_color)
    durations = [800] * N               # 800ms per frame, except...
    durations[0] //= 2                  # first frame is shorter
    durations[-1] *= 1.25               # final frame is longer

    save_animated_gif("output/SierpinskiCarpet.gif", carpets, durations)

if __name__ == '__main__':
    main()