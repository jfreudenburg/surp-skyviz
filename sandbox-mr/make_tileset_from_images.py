"""Code to generate slippymap-like tiles from a series of images 
assuming that the image is perfectly square
"""

import numpy as np
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from numpy.lib.shape_base import tile


def make_tileset_from_images(path, img_dict, tile_size=256, min_zoom=0):
    """Make all the tiles (and required directories) for a slippymap series of tiles

    Args:
        path (str): Path to create directory structure. Path does not have to exist.
        img_dict (dict): A dictionary with entires in the form of {zoom_level(int): path_to_image (str)}.
        tile_size (int, optional): Size of square tile in pixels. Defaults to 256.
        min_zoom (int, optional): Minimum zoom level to generate. 
    """

    # Making the Root Directory
    rootdir = Path(path)

    if not rootdir.exists():
        rootdir.mkdir(parents=True, exist_ok=True)

    print("Writing Image Tiles to: %s" % rootdir)

    # Getting a range of the min and max zoom levels:
    specified_zooms = list(img_dict.keys())
    specified_zooms.sort()
    max_zoom = np.max(specified_zooms)
    zoom_inds = range(min_zoom, max_zoom)

    print("Images defined for the following zoom levels: %s" % specified_zooms)

    # Running through Zoom Levels
    for i_zoom in zoom_inds:

        n_slices_1d = 2 ** i_zoom
        scaled_im_size = n_slices_1d * tile_size

        # Identifying the correct image to use for this zoom level
        img_ind = np.where(specified_zooms >= i_zoom)[0].min()
        raw_image_fname = img_dict[specified_zooms[img_ind]]
        raw_image = Image.open(raw_image_fname)

        if raw_image.size[0] != raw_image.size[1]:
            raise AssertionError(
                "Image does not have dimensions that are square (%i, %i)"
                % raw_image.size
            )

        print("Generating Slices for Zoom Level %i" % i_zoom)
        print(
            "Number of Slices/Pixels in each dimension %i slices/%i px "
            % (n_slices_1d, scaled_im_size)
        )

        # Resizing Image to correct overall tile size:
        scaled_im = raw_image.resize(
            (scaled_im_size, scaled_im_size), resample=Image.BICUBIC
        )

        for i_x in range(n_slices_1d):
            for i_y in range(n_slices_1d):
                print("\tGenerating tile (%i, %i)" % (i_x, i_y))
                clip_im = clip_image_from_zoom(scaled_im, i_x, i_y, tile_size=tile_size)
                save_image_tile(rootdir, i_zoom, i_x, i_y, clip_im)


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


def save_image_tile(rootdir, zoom_level, x, y, image):
    """Saves the image tile as a png, making all directories if necessary

    Args:
        rootdir (pathlib Path): Root Path to where the image tile should be saved to
        zoom_level (int): Zoom level of the image tile
        x (int): X-index of the tile
        y (int): Y-index of the tile
        image (Pillow Image): Image Tile to save
    """

    fpath = rootdir / str(zoom_level) / str(x)

    if not fpath.exists():
        fpath.mkdir(parents=True, exist_ok=True)

    fname = fpath / (str(y) + ".png")

    image.save(fname)

