from astropy.constants import c
from astropy.coordinates import Galactic
import warnings
import os
import PIL
import numpy as np
import healpy as hp
from healpy.projaxes import HistEqNorm
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
from mycmap import get_continuous_cmap

def generate_projection_set(m,size,dname,coord=['G'],cmap='viridis',norm='hist'):
    """
    Generate a set of 6 square, unpadded orthographic projections of a 
    healpix map, with centers at the following lon/lat:

    (0,90)  / (0,-90)    North pole / South pole
    (0,0)   / (180/0)    centered on equator
    (45,45) / (215,-45)  off-axis

    Parameters
    ----------
    m : ndarray
        healpix array to be mapped

    size : int
        width of each image in pixels

    dname : str
        name of directory to contain output images

    coord : sequence of character
        Either one of ‘G’, ‘E’ or ‘C’ to describe the coordinate system of 
        the map, or a sequence of 2 of these to rotate the map from the 
        first to the second coordinate system. (default "G")

    norm : {‘hist’, ‘log’, None}
        Color normalization, hist= histogram equalized color mapping, log= logarithmic color mapping, 
        default: None (linear color mapping)
    
    cmap : a color map
        The colormap to use (see matplotlib.cm)
    
    Returns
    -------
    Creates a directory named as specified by dname. Saves square, axis-free, transparent-background images 
    of the orthographic projection of map m with edge size in pixels as specified by size parameter. Image names 
    correspond to projection centers as follows:
    North Pole     - (0,90)
    South Pole     - (0,-90)
    Prime Meridian - (0,0)
    Antimeridian   - (180,0)
    Off-axis       - (45,45)
    Anti-off-axis  - (215,-45)

    """
    
    # Check whether size is power of 2
    if not np.ceil(np.log2(size))==np.log2(size):
        warnings.warn("Image size is not a power of 2")
    
    # Check if directory exists, make _copy if not, make directory
    def unique_dname(dname):
        if os.path.exists(os.path.join(os.getcwd(),dname)):
            warnings.warn("Directory already exists; ")
            return unique_dname(dname+'_copy')
        else:
            return dname
    
    dirname = unique_dname(dname)
    os.mkdir(dirname)

    centers = [(0,90),
               (0.0),
               (45,45)]
    fnames = [('northpole','southpole'),
              ('primemeridian','antimeridian'),
              ('offaxis','antioffaxis')]

    for i,rot in enumerate(centers):
        image_linear = hp.orthview(m,rot=rot,xsize=2*size,coord=coord,return_projected_map=True,cmap=cmap,norm=norm,min=0)
        
        if norm=='hist':
            # renormalize with histogram equalization
            img[img==-np.inf] = np.nan
            vmin = 0
            vmax = img[~np.isnan(img)].max()
            normalized = HistEqNorm(vmin=vmin,vmax=vmax)
            
        
        elif norm=='log':
            warnings.warn('Log normalization not yet implemented')
        
        plt.imsave(fname=dirname+'/'+fnames[i][0]+'.png',
                   arr=cmap(normalized(image[:,:size])),
                   vmin=vmin,
                   vmax=vmax,
                   origin='lower',
                   cmap=cmap,
                   format='png')

        plt.imsave(fname=dirname+'/'+fnames[i][1]+'.png',
                   arr=cmap(normalized(image[:,size:])),
                   vmin=vmin,
                   vmax=vmax,
                   origin='lower',
                   cmap=cmap,
                   format='png')


if __name__=="__main__":
    lon = 215
    lat = -45
    print('lat: {:0.2f} \nlon: {:0.2f}'.format(lat,lon))

    ns = 16
    test_map = np.arange(hp.nside2npix(ns))

    ipix = hp.ang2pix(ns,np.pi/2-np.pi*lat/180,np.pi*lon/180)
    test_map[ipix] = 1.5*test_map.max()

    generate_projection_set(test_map,512,'testset')