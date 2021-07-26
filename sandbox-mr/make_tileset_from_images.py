"""Code to generate slippymap-like tiles from a series of images 
assuming that the image is perfectly square
"""

import numpy as np
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont


def make_tileset_from_images(path, img_dict, tile_size=256, min_zoom=0):
    """Make all the tiles (and required directories) for a slippymap series of tiles

    Args:
        path (str): Path to create directory structure. Path does not have to exist.
        img_dict (dict): A dictionary with entires in the form of {zoom_level(int): path_to_image (str)}.
        tile_size (int, optional): Size of square tile in pixels. Defaults to 256.
        min_zoom (int, optional): Minimum zoom level to generate. 
    """
    pass


def clip_image_from_zoom(im, ix, iy, tile_size=256):
    """Clip tile from larger image

    Args:
        im (Pillow Image): Full-sized image
        ix (int): Tile Index (x-direction)
        iy (int): Tile Index (y-direction)
        tile_size (int, optional): Size of Tile in Pixels. Defaults to 256.

    Returns:
        Pillow Image: Tile Image
    """
    minx = tile_size * ix
    maxx = tile_size * (ix + 1)
    miny = tile_size * iy
    maxy = tile_size(ix + 1)
    return im.crop((minx, miny, maxx, maxy))
