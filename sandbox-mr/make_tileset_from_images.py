"""Code to generate slippymap-like tiles from a series of images 
assuming that the image is perfectly square
"""

import numpy as np
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont


def make_tileset_from_images(
    path, img_dict, tile_size=256,
):
    """Make all the tiles (and required directories) for a slippymap series of tiles

    Args:
        path (str): Path to create directory structure. Path does not have to exist.
        img_dict (dict): A dictionary with entires in the form of {zoom_level(int): path_to_image (str)}.
        tile_size (int, optional): Size of square tile in pixels. Defaults to 256.
    """
    pass

